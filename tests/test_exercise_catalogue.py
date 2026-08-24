from sqlalchemy.orm import Session

from fitpilot.db.models import Exercise
from fitpilot.services.exercise_catalogue import get_exercise_by_name


def test_get_exercise_by_name_returns_matching_exercise(
    db_session: Session,
) -> None:
    exercise = Exercise(
        name="Bench Press",
        required_equipment="barbell",
        movement_category="push",
        difficulty="intermediate",
    )

    db_session.add(exercise)
    db_session.commit()

    result = get_exercise_by_name(db_session, "Bench Press")

    assert result is not None
    assert result.name == "Bench Press"
    assert result.required_equipment == "barbell"
