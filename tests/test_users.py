from fastapi.testclient import TestClient

from fitpilot.main import app

client = TestClient(app)


def test_create_valid_user_profile() -> None:
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
    assert response.json()["name"] == "Test User"
    assert response.json()["goal"] == "fat_loss_and_strength"


def test_create_user_profile_rejects_invalid_age() -> None:
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
