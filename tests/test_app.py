import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Soccer Team" in data
    assert "participants" in data["Soccer Team"]

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    activity = "Art Club"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_for_activity_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Math Olympiad"
    # Sign up once
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Try to sign up again
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "foo@bar.com"})
    assert response.status_code == 404

def test_unregister_from_activity_success():
    email = "unregister@mergington.edu"
    activity = "Science Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

def test_unregister_not_registered():
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

def test_unregister_from_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "foo@bar.com"})
    assert response.status_code == 404
