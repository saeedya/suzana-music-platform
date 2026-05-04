from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_db

client = TestClient(app)


def test_signup_success():
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.id = "123"
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.is_admin = False
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    app.dependency_overrides[get_db] = lambda: mock_db

    with patch("app.api.auth.sign_up") as mock_signup:
        mock_signup.return_value = {
            "user": {"email": "test@example.com"},
            "session": MagicMock(access_token="token"),
        }
        response = client.post("/api/v1/auth/signup", json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "password123",
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["user"]["email"] == "test@example.com"

    app.dependency_overrides.clear()

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
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.id = "123"
    mock_user.email = "test@example.com"
    mock_user.full_name = "Test User"
    mock_user.is_admin = False
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    app.dependency_overrides[get_db] = lambda: mock_db

    with patch("app.api.auth.sign_in") as mock_signin:
        mock_signin.return_value = {
            "user": {"email": "test@example.com"},
            "session": MagicMock(access_token="token"),
        }
        response = client.post("/api/v1/auth/signin", json={
            "email": "test@example.com",
            "password": "password123",
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["user"]["email"] == "test@example.com"

    app.dependency_overrides.clear()


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