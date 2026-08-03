import os
import sys
import unittest
from unittest.mock import MagicMock, patch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import service


class TestProcessUsers(unittest.TestCase):
    @patch("app.service.update_user")
    @patch("app.service.assign_license")
    @patch("app.service.has_license", return_value=False)
    @patch("app.service.find_user_by_upn")
    @patch("app.service.find_license_by_code")
    @patch("app.service.get_licenses")
    @patch("app.service.get_users")
    @patch("app.service.get_pending_users")
    def test_assigns_license_for_eligible_user(
        self,
        get_pending_users,
        get_users,
        get_licenses,
        find_license_by_code,
        find_user_by_upn,
        has_license,
        assign_license,
        update_user,
    ):
        get_pending_users.return_value = [(1, "alice@example.com")]
        get_users.return_value = [
            {
                "userPrincipalName": "alice@example.com",
                "id": "user-1",
                "accountEnabled": True,
                "assignedLicenses": [],
            }
        ]
        get_licenses.return_value = [{"license": {"code": "E3", "id": "license-1"}}]
        find_license_by_code.return_value = {"code": "E3", "id": "license-1"}
        find_user_by_upn.return_value = get_users.return_value[0]

        service.process_users()

        assign_license.assert_called_once_with("user-1", "license-1")
        update_user.assert_called_once_with(
            user_id=1,
            status="ASSIGNED",
            message="License assigned successfully",
            api_user_id="user-1",
        )

    @patch("app.service.update_user")
    @patch("app.service.find_license_by_code", return_value=None)
    @patch("app.service.get_licenses")
    @patch("app.service.get_users")
    @patch("app.service.get_pending_users")
    def test_raises_when_license_not_found(
        self,
        get_pending_users,
        get_users,
        get_licenses,
        find_license_by_code,
        update_user,
    ):
        get_pending_users.return_value = [(1, "alice@example.com")]
        get_users.return_value = []
        get_licenses.return_value = []

        with self.assertRaises(Exception) as context:
            service.process_users()

        self.assertIn("License '", str(context.exception))
        update_user.assert_not_called()

    @patch("app.service.update_user")
    @patch("app.service.has_license", return_value=False)
    @patch("app.service.find_user_by_upn", return_value=None)
    @patch("app.service.find_license_by_code")
    @patch("app.service.get_licenses")
    @patch("app.service.get_users")
    @patch("app.service.get_pending_users")
    def test_marks_not_found_for_missing_user(
        self,
        get_pending_users,
        get_users,
        get_licenses,
        find_license_by_code,
        find_user_by_upn,
        has_license,
        update_user,
    ):
        get_pending_users.return_value = [(2, "missing@example.com")]
        get_users.return_value = []
        get_licenses.return_value = [{"license": {"code": "E3", "id": "license-1"}}]
        find_license_by_code.return_value = {"code": "E3", "id": "license-1"}

        service.process_users()

        update_user.assert_called_once_with(
            user_id=2,
            status="NOT_FOUND",
            message="User not found",
        )

    @patch("app.service.update_user")
    @patch("app.service.has_license", return_value=False)
    @patch("app.service.find_user_by_upn")
    @patch("app.service.find_license_by_code")
    @patch("app.service.get_licenses")
    @patch("app.service.get_users")
    @patch("app.service.get_pending_users")
    def test_marks_disabled_user(
        self,
        get_pending_users,
        get_users,
        get_licenses,
        find_license_by_code,
        find_user_by_upn,
        has_license,
        update_user,
    ):
        get_pending_users.return_value = [(3, "disabled@example.com")]
        get_users.return_value = [
            {
                "userPrincipalName": "disabled@example.com",
                "id": "user-3",
                "accountEnabled": False,
                "assignedLicenses": [],
            }
        ]
        get_licenses.return_value = [{"license": {"code": "E3", "id": "license-1"}}]
        find_license_by_code.return_value = {"code": "E3", "id": "license-1"}
        find_user_by_upn.return_value = get_users.return_value[0]

        service.process_users()

        update_user.assert_called_once_with(
            user_id=3,
            status="DISABLED",
            message="User is disabled",
            api_user_id="user-3",
        )

    @patch("app.service.update_user")
    @patch("app.service.assign_license")
    @patch("app.service.has_license", return_value=True)
    @patch("app.service.find_user_by_upn")
    @patch("app.service.find_license_by_code")
    @patch("app.service.get_licenses")
    @patch("app.service.get_users")
    @patch("app.service.get_pending_users")
    def test_marks_already_assigned_user(
        self,
        get_pending_users,
        get_users,
        get_licenses,
        find_license_by_code,
        find_user_by_upn,
        has_license,
        assign_license,
        update_user,
    ):
        get_pending_users.return_value = [(4, "assigned@example.com")]
        get_users.return_value = [
            {
                "userPrincipalName": "assigned@example.com",
                "id": "user-4",
                "accountEnabled": True,
                "assignedLicenses": [{"skuId": "license-1"}],
            }
        ]
        get_licenses.return_value = [{"license": {"code": "E3", "id": "license-1"}}]
        find_license_by_code.return_value = {"code": "E3", "id": "license-1"}
        find_user_by_upn.return_value = get_users.return_value[0]

        service.process_users()

        assign_license.assert_not_called()
        update_user.assert_called_once_with(
            user_id=4,
            status="ALREADY_ASSIGNED",
            message="License already assigned",
            api_user_id="user-4",
        )

    @patch("app.service.update_user")
    @patch("app.service.assign_license", side_effect=Exception("assignment failed"))
    @patch("app.service.has_license", return_value=False)
    @patch("app.service.find_user_by_upn")
    @patch("app.service.find_license_by_code")
    @patch("app.service.get_licenses")
    @patch("app.service.get_users")
    @patch("app.service.get_pending_users")
    def test_marks_failed_on_assignment_exception(
        self,
        get_pending_users,
        get_users,
        get_licenses,
        find_license_by_code,
        find_user_by_upn,
        has_license,
        assign_license,
        update_user,
    ):
        get_pending_users.return_value = [(5, "alice@example.com")]
        get_users.return_value = [
            {
                "userPrincipalName": "alice@example.com",
                "id": "user-5",
                "accountEnabled": True,
                "assignedLicenses": [],
            }
        ]
        get_licenses.return_value = [{"license": {"code": "E3", "id": "license-1"}}]
        find_license_by_code.return_value = {"code": "E3", "id": "license-1"}
        find_user_by_upn.return_value = get_users.return_value[0]

        service.process_users()

        update_user.assert_called_once_with(
            user_id=5,
            status="FAILED",
            message="assignment failed",
            api_user_id="user-5",
        )


if __name__ == "__main__":
    unittest.main()
