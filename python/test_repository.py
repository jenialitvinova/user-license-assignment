from app.repository import get_pending_users


def main():
    users = get_pending_users()

    print(f"Pending users: {len(users)}")
    print(users[:3])


if __name__ == "__main__":
    main()