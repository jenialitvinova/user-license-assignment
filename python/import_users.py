import csv

from app.database import get_connection


def import_users(csv_path: str):
    connection = get_connection()
    cursor = connection.cursor()

    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT INTO users (user_principal_name)
                VALUES (%s)
                ON CONFLICT (user_principal_name) DO NOTHING
                """,
                (row["UserPrincipalName"],),
            )

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    import_users("../data/users_graph.csv")
    print("Import completed.")