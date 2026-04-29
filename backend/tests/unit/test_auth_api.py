from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_signup_success():
    with patch("app.api.auth.sign_up") as mock:
        mock.return_value = {"user": {"email": "test@example.com"}, "session": {}}
        response = client.post("/api/v1/auth/signup", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "password123",
        })
        assert response.status_code == 200
        assert "user" in response.json()


def test_signup_failure():
    with patch("app.api.auth.sign_up") as mock:
        mock.side_effect = Exception("Email already registered")
        response = client.post("/api/v1/auth/signup", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "password123",
        })
        assert response.status_code == 400


def test_signin_success():
    with patch("app.api.auth.sign_in") as mock:
        mock.return_value = {"user": {"email": "test@example.com"}, "session": {"access_token": "token"}}
        response = client.post("/api/v1/auth/signin", json={
            "email": "test@example.com",
            "password": "password123",
        })
        assert response.status_code == 200
        assert "session" in response.json()


def test_signin_failure():
    with patch("app.api.auth.sign_in") as mock:
        mock.side_effect = Exception("Invalid credentials")
        response = client.post("/api/v1/auth/signin", json={
            "email": "test@example.com",
            "password": "wrongpassword",
        })
        assert response.status_code == 401


def test_signout_success():
    with patch("app.api.auth.sign_out") as mock:
        mock.return_value = None
        response = client.post("/api/v1/auth/signout", json={
            "jwt": "some-valid-jwt",
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Signed out successfully"

def test_signout_failure():
    with patch("app.api.auth.sign_out") as mock:
        mock.side_effect = Exception("Sign out failed")
        response = client.post("/api/v1/auth/signout", json={
            "jwt": "invalid-jwt",
        })
        assert response.status_code == 400