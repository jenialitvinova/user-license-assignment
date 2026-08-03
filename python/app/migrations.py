import os
from pathlib import Path

import psycopg

from app.config import DB_CONFIG

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "database" / "migrations"


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def applied_migrations(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(50) PRIMARY KEY,
                applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute("SELECT version FROM schema_migrations ORDER BY version")
        return {row[0] for row in cursor.fetchall()}


def apply_migration(connection, migration_file: Path):
    with migration_file.open("r", encoding="utf-8") as file:
        sql = file.read()

    with connection.cursor() as cursor:
        cursor.execute(sql)
        cursor.execute(
            "INSERT INTO schema_migrations (version) VALUES (%s)",
            (migration_file.name,)
        )


def run_migrations():
    connection = get_connection()
    try:
        applied = applied_migrations(connection)
        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

        for migration_file in migration_files:
            if migration_file.name in applied:
                continue

            print(f"Applying migration: {migration_file.name}")
            apply_migration(connection, migration_file)

        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    run_migrations()
