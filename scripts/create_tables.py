from fitpilot.db.base import Base
from fitpilot.db.models import User  # noqa: F401
from fitpilot.db.session import engine


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")


if __name__ == "__main__":
    main()
