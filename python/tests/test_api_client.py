import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import api_client


class TestApiClient(unittest.TestCase):
    def test_find_user_by_upn_matches_case_insensitive(self):
        users = [{"userPrincipalName": "Alice@Example.Com"}]
        result = api_client.find_user_by_upn(users, "alice@example.com")

        self.assertEqual(result, users[0])

    def test_find_user_by_upn_returns_none_if_no_match(self):
        result = api_client.find_user_by_upn([], "missing@example.com")

        self.assertIsNone(result)

    def test_find_license_by_code_matches_nested_license_and_case_insensitive(self):
        licenses = [
            {"license": {"code": "e3", "id": "license-1"}},
            {"license": {"code": "e5", "id": "license-2"}},
        ]

        result = api_client.find_license_by_code(licenses, "E3")

        self.assertEqual(result, {"code": "e3", "id": "license-1"})

    def test_find_license_by_code_returns_none_if_missing(self):
        licenses = [{"license": {"code": "e5", "id": "license-2"}}]

        result = api_client.find_license_by_code(licenses, "e3")

        self.assertIsNone(result)

    def test_has_license_returns_true_when_license_exists(self):
        api_user = {"assignedLicenses": [{"skuId": "license-1"}]}

        self.assertTrue(api_client.has_license(api_user, "license-1"))

    def test_has_license_returns_false_when_license_missing(self):
        api_user = {"assignedLicenses": [{"skuId": "license-1"}]}

        self.assertFalse(api_client.has_license(api_user, "license-2"))


if __name__ == "__main__":
    unittest.main()
