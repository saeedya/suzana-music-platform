import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.core.dependencies import get_admin_user, get_current_user, get_db
from app.main import app

client = TestClient(app)


def mock_admin():
    user = MagicMock()
    user.is_admin = True
    return user


def mock_user():
    return MagicMock()


def test_create_availability():
    app.dependency_overrides[get_db] = lambda: MagicMock()
    app.dependency_overrides[get_admin_user] = mock_admin

    with patch("app.api.availability.create_availability") as mock:
        mock.return_value = MagicMock(
            id=uuid.uuid4(),
            day_of_week=0,
            start_time="09:00:00",
            end_time="17:00:00",
            session_duration=60,
            is_active=True,
            timezone="America/New_York",
        )
        response = client.post(
            "/api/v1/availability/",
            json={
                "day_of_week": 0,
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "session_duration": 60,
                "timezone": "America/New_York",
            },
        )
        assert response.status_code == 200

    app.dependency_overrides.clear()


def test_list_availability():
    app.dependency_overrides[get_db] = lambda: MagicMock()

    with patch("app.api.availability.get_availability") as mock:
        mock.return_value = []
        response = client.get("/api/v1/availability/")
        assert response.status_code == 200
        assert response.json() == []

    app.dependency_overrides.clear()


def test_get_slots():
    app.dependency_overrides[get_db] = lambda: MagicMock()
    app.dependency_overrides[get_current_user] = mock_user

    with patch("app.api.availability.get_available_slots") as mock:
        mock.return_value = []
        response = client.get(
            "/api/v1/availability/slots?target_date=2026-05-11&session_duration=60"
        )
        assert response.status_code == 200

    app.dependency_overrides.clear()


def test_get_slots_invalid_duration():
    app.dependency_overrides[get_db] = lambda: MagicMock()
    app.dependency_overrides[get_current_user] = mock_user

    response = client.get(
        "/api/v1/availability/slots?target_date=2026-05-11&session_duration=45"
    )
    assert response.status_code == 400

    app.dependency_overrides.clear()