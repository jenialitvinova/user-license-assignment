import os
import sys
import unittest
from unittest.mock import MagicMock, patch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import repository


class TestRepository(unittest.TestCase):
    @patch("app.repository.get_connection")
    def test_get_pending_users_returns_rows(self, get_connection):
        cursor = MagicMock()
        cursor.fetchall.return_value = [(1, "alice@example.com")]

        connection = MagicMock()
        connection.cursor.return_value = cursor
        get_connection.return_value = connection

        result = repository.get_pending_users()

        cursor.execute.assert_called_once()
        cursor.close.assert_called_once()
        connection.close.assert_called_once()
        self.assertEqual(result, [(1, "alice@example.com")])

    @patch("app.repository.get_connection")
    def test_update_user_commits_and_closes_connection(self, get_connection):
        cursor = MagicMock()
        connection = MagicMock()
        connection.cursor.return_value = cursor
        get_connection.return_value = connection

        repository.update_user(
            user_id=42,
            status="ASSIGNED",
            message="OK",
            api_user_id="user-42",
        )

        cursor.execute.assert_called_once_with(
            """
        UPDATE users
        SET
            status = %s,
            message = %s,
            api_user_id = %s,
            processed_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
            ("ASSIGNED", "OK", "user-42", 42),
        )
        connection.commit.assert_called_once()
        cursor.close.assert_called_once()
        connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
