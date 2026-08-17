from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from fitpilot.db.models import Equipment, User


def test_create_valid_user_profile(client: TestClient) -> None:
    payload = {
        "name": "Test User",
        "age": 29,
        "height_cm": 173,
        "weight_kg": 100,
        "goal": "fat_loss_and_strength",
        "experience_level": "beginner",
        "training_days_per_week": 3,
        "available_equipment": ["dumbbells", "machines"],
        "exercise_limitations": ["avoid_high_impact"],
    }

    response = client.post("/users/profile", json=payload)

    assert response.status_code == 201

    body = response.json()

    assert body["id"] == 1
    assert body["name"] == "Test User"
    assert body["goal"] == "fat_loss_and_strength"


def test_create_user_profile_rejects_invalid_age(
    client: TestClient,
) -> None:
    payload = {
        "name": "Test User",
        "age": -5,
        "height_cm": 173,
        "weight_kg": 100,
        "goal": "fat_loss",
        "experience_level": "beginner",
        "training_days_per_week": 3,
        "available_equipment": [],
        "exercise_limitations": [],
    }

    response = client.post("/users/profile", json=payload)

    assert response.status_code == 422


def test_get_existing_user_profile(client: TestClient) -> None:
    payload = {
        "name": "Test User",
        "age": 29,
        "height_cm": 173,
        "weight_kg": 100,
        "goal": "fat_loss",
        "experience_level": "beginner",
        "training_days_per_week": 3,
        "available_equipment": [],
        "exercise_limitations": [],
    }

    create_response = client.post("/users/profile", json=payload)

    user_id = create_response.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Test User"


def test_get_missing_user_returns_404(client: TestClient) -> None:
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_create_user_profile_persists_normalized_equipment(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/users/profile",
        json={
            "name": "Equipment Test",
            "age": 29,
            "height_cm": 175,
            "weight_kg": 100,
            "goal": "fat_loss",
            "experience_level": "intermediate",
            "training_days_per_week": 4,
            "available_equipment": [
                " Dumbbells ",
                "BARBELL",
                "machines",
                "   ",
            ],
            "exercise_limitations": [],
        },
    )

    assert response.status_code == 201

    equipment = db_session.scalars(select(Equipment).order_by(Equipment.name)).all()

    equipment_names = [item.name for item in equipment]

    assert equipment_names == [
        "barbell",
        "dumbbells",
        "machines",
    ]


def test_create_user_profile_persists_cleaned_exercise_limitations(
    client: TestClient,
    db_session: Session,
) -> None:
    response = client.post(
        "/users/profile",
        json={
            "name": "Limitation Test",
            "age": 29,
            "height_cm": 175,
            "weight_kg": 100,
            "goal": "fat_loss",
            "experience_level": "intermediate",
            "training_days_per_week": 4,
            "available_equipment": [],
            "exercise_limitations": [
                " knee pain ",
                "Avoid overhead press",
                "   ",
            ],
        },
    )

    assert response.status_code == 201

    user = db_session.scalar(select(User).where(User.name == "Limitation Test"))

    assert user is not None
    assert user.exercise_limitations == [
        "knee pain",
        "Avoid overhead press",
    ]
