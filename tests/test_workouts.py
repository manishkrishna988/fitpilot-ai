from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from fitpilot.db.models import PlannedExercise, User, WorkoutDay


def test_create_workout_plan_generates_five_day_template(
    client: TestClient,
    db_session: Session,
) -> None:
    user = User(
        name="Workout Test User",
        age=29,
        height_cm=175,
        weight_kg=100,
        goal="strength",
        experience_level="intermediate",
        training_days_per_week=5,
        exercise_limitations=[],
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.post(
        "/workout-plans",
        json={
            "user_id": user.id,
            "week_start_date": "2026-08-24",
        },
    )

    assert response.status_code == 201

    workout_days = db_session.scalars(
        select(WorkoutDay).order_by(WorkoutDay.day_number)
    ).all()

    day_names = [day.name for day in workout_days]

    assert day_names == [
        "Push",
        "Pull",
        "Legs",
        "Upper",
        "Lower",
    ]

    planned_exercises = db_session.scalars(
        select(PlannedExercise).order_by(PlannedExercise.id)
    ).all()

    assert len(planned_exercises) == 15

    exercise_names = [exercise.name for exercise in planned_exercises]

    assert exercise_names == [
        "Bench Press",
        "Incline Dumbbell Press",
        "Triceps Pushdown",
        "Lat Pulldown",
        "Seated Row",
        "Biceps Curl",
        "Leg Press",
        "Leg Curl",
        "Leg Extension",
        "Bench Press",
        "Seated Row",
        "Shoulder Press",
        "Leg Press",
        "Leg Curl",
        "Calf Raise",
    ]


def test_create_workout_plan_rejects_unsupported_training_frequency(
    client: TestClient,
    db_session: Session,
) -> None:
    user = User(
        name="Unsupported Frequency User",
        age=29,
        height_cm=175,
        weight_kg=100,
        goal="strength",
        experience_level="beginner",
        training_days_per_week=2,
        exercise_limitations=[],
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.post(
        "/workout-plans",
        json={
            "user_id": user.id,
            "week_start_date": "2026-08-24",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "No workout template available for this training frequency"
    }
