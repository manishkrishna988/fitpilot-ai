from fastapi.testclient import TestClient


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
