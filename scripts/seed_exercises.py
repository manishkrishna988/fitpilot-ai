from sqlalchemy import select

from fitpilot.db.models import Exercise
from fitpilot.db.session import SessionLocal

EXERCISES = [
    Exercise(
        name="Bench Press",
        required_equipment="barbell",
        movement_category="push",
        difficulty="intermediate",
    ),
    Exercise(
        name="Incline Dumbbell Press",
        required_equipment="dumbbells",
        movement_category="push",
        difficulty="intermediate",
    ),
    Exercise(
        name="Lat Pulldown",
        required_equipment="cable_machine",
        movement_category="pull",
        difficulty="beginner",
    ),
]


def main() -> None:
    with SessionLocal() as db:
        for exercise in EXERCISES:
            existing = db.scalar(select(Exercise).where(Exercise.name == exercise.name))

            if existing is None:
                db.add(exercise)

        db.commit()


if __name__ == "__main__":
    main()
