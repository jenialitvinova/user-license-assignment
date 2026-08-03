import logging

from app import api_client
from app import repository
from app.config import LICENSE_CODE


def process_users():
    pending_users = repository.get_pending_users()
    api_users = api_client.get_users()
    licenses = api_client.get_licenses()

    license_info = api_client.find_license_by_code(
        licenses,
        LICENSE_CODE,
    )

    if license_info is None:
        raise ValueError(f"License '{LICENSE_CODE}' not found")

    license_id = license_info["id"]

    for user_id, user_principal_name in pending_users:
        api_user = api_client.find_user_by_upn(
            api_users,
            user_principal_name,
        )

        if api_user is None:
            repository.update_user(
                user_id=user_id,
                status="NOT_FOUND",
                message="User not found",
            )

            logging.info(f"{user_principal_name} -> NOT_FOUND")
            continue

        if not api_user["accountEnabled"]:
            repository.update_user(
                user_id=user_id,
                status="DISABLED",
                message="User is disabled",
                api_user_id=api_user["id"],
            )

            logging.info(f"{user_principal_name} -> DISABLED")
            continue

        if api_client.has_license(api_user, license_id):
            repository.update_user(
                user_id=user_id,
                status="ALREADY_ASSIGNED",
                message="License already assigned",
                api_user_id=api_user["id"],
            )

            logging.info(f"{user_principal_name} -> ALREADY_ASSIGNED")
            continue

        try:
            api_client.assign_license(api_user["id"], license_id)

            repository.update_user(
                user_id=user_id,
                status="ASSIGNED",
                message="License assigned successfully",
                api_user_id=api_user["id"],
            )

            logging.info(f"{user_principal_name} -> ASSIGNED")

        except Exception as e:
            repository.update_user(
                user_id=user_id,
                status="FAILED",
                message=str(e),
                api_user_id=api_user["id"],
            )

            logging.error(f"{user_principal_name} -> FAILED: {e}")