import logging

from app.api_client import (
    assign_license,
    find_license_by_code,
    find_user_by_upn,
    get_licenses,
    get_users,
    has_license,
)
from app.config import LICENSE_CODE
from app.repository import get_pending_users, update_user


def process_users():
    pending_users = get_pending_users()
    api_users = get_users()
    licenses = get_licenses()

    license_info = find_license_by_code(
        licenses,
        LICENSE_CODE,
    )

    if license_info is None:
        raise Exception(f"License '{LICENSE_CODE}' not found")

    license_id = license_info["id"]

    for user_id, user_principal_name in pending_users:
        api_user = find_user_by_upn(api_users, user_principal_name)

        if api_user is None:
            update_user(
                user_id=user_id,
                status="NOT_FOUND",
                message="User not found",
            )

            logging.info(f"{user_principal_name} -> NOT_FOUND")
            continue

        if not api_user["accountEnabled"]:
            update_user(
                user_id=user_id,
                status="DISABLED",
                message="User is disabled",
                api_user_id=api_user["id"],
            )

            logging.info(f"{user_principal_name} -> DISABLED")
            continue

        if has_license(api_user, license_id):
            update_user(
                user_id=user_id,
                status="ALREADY_ASSIGNED",
                message="License already assigned",
                api_user_id=api_user["id"],
            )

            logging.info(f"{user_principal_name} -> ALREADY_ASSIGNED")
            continue

        try:
            assign_license(api_user["id"], license_id)

            update_user(
                user_id=user_id,
                status="ASSIGNED",
                message="License assigned successfully",
                api_user_id=api_user["id"],
            )

            logging.info(f"{user_principal_name} -> ASSIGNED")

        except Exception as e:
            update_user(
                user_id=user_id,
                status="FAILED",
                message=str(e),
                api_user_id=api_user["id"],
            )

            logging.error(f"{user_principal_name} -> FAILED: {e}")