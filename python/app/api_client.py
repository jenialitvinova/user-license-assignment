import requests

from app.config import API_BASE_URL


def get_users():
    response = requests.get(f"{API_BASE_URL}/v1/users")
    response.raise_for_status()
    return response.json()["value"]


def get_licenses():
    response = requests.get(f"{API_BASE_URL}/v1/licenses")
    response.raise_for_status()
    return response.json()["value"]


def assign_license(user_id: str, license_id: str):
    response = requests.post(
        f"{API_BASE_URL}/v1/users/{user_id}/licenses",
        json={"licenseId": license_id},
    )
    response.raise_for_status()
    return response.json()


def find_user_by_upn(users: list, user_principal_name: str):
    user_principal_name = user_principal_name.lower()

    for user in users:
        if user["userPrincipalName"].lower() == user_principal_name:
            return user

    return None


def find_license_by_code(licenses: list, code: str):
    code = code.upper()

    for item in licenses:
        if "license" in item:
            current = item["license"]
        else:
            current = item

        if current["code"].upper() == code:
            return current

    return None


def has_license(api_user: dict, license_id: str):
    for assigned in api_user["assignedLicenses"]:
        if assigned["skuId"] == license_id:
            return True

    return False