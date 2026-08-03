from app.database import get_connection


def get_pending_users():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, user_principal_name
        FROM users
        WHERE status = 'PENDING'
        ORDER BY id
        """
    )

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users


def update_user(
    user_id: int,
    status: str,
    message: str | None = None,
    api_user_id: str | None = None,
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET
            status = %s,
            message = %s,
            api_user_id = %s,
            processed_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
        (status, message, api_user_id, user_id),
    )

    connection.commit()

    cursor.close()
    connection.close()