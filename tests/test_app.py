import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("description" in v for v in data.values())


def test_signup_and_unregister():
    # Use a test activity and email
    response = client.get("/activities")
    activities = response.json()
    activity_name = next(iter(activities.keys()))
    email = "pytestuser@mergington.edu"

    # Sign up
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert "message" in response.json()

    # Duplicate signup should fail or not add again
    response_dup = client.post(signup_url)
    assert response_dup.status_code != 500

    # Unregister
    unregister_url = f"/activities/{activity_name}/unregister?email={email}"
    response = client.post(unregister_url)
    assert response.status_code == 200
    assert "message" in response.json()

    # Unregister again should not fail
    response_dup = client.post(unregister_url)
    assert response_dup.status_code != 500
