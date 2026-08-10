from sqlalchemy import text

from fitpilot.db.session import engine


def main() -> None:
    with engine.connect() as connection:
        database_name = connection.execute(
            text("SELECT current_database();")
        ).scalar_one()

        database_user = connection.execute(text("SELECT current_user;")).scalar_one()

        print(f"Connected database: {database_name}")
        print(f"Connected user: {database_user}")


if __name__ == "__main__":
    main()
