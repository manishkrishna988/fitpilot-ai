from sqlalchemy import select
from sqlalchemy.orm import Session

from fitpilot.db.models import Exercise


def get_exercise_by_name(
    db: Session,
    exercise_name: str,
) -> Exercise | None:
    return db.scalar(select(Exercise).where(Exercise.name == exercise_name))
