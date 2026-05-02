import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.core.dependencies import get_admin_user, get_current_user
from app.main import app

client = TestClient(app)


def make_mock_user(is_admin: bool = False) -> MagicMock:
    user = MagicMock()
    user.id = uuid.uuid4()
    user.is_admin = is_admin
    user.is_active = True
    return user


def make_booking_response() -> dict:
    return {
        "id": str(uuid.uuid4()),
        "student_id": str(uuid.uuid4()),
        "instrument_id": str(uuid.uuid4()),
        "starts_at": datetime.now(timezone.utc).isoformat(),
        "ends_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
        "price_cents": 5000,
        "notes": None,
        "stripe_payment_intent_id": None,
        "daily_room_url": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def test_book_lesson_success():
    app.dependency_overrides[get_current_user] = lambda: make_mock_user()
    with patch("app.api.bookings.create_booking") as mock:
        mock.return_value = make_booking_response()
        response = client.post("/api/v1/bookings/", json={
            "instrument_id": str(uuid.uuid4()),
            "starts_at": datetime.now(timezone.utc).isoformat(),
            "ends_at": datetime.now(timezone.utc).isoformat(),
            "price_cents": 5000,
        })
        assert response.status_code == 200
    app.dependency_overrides.clear()


def test_book_lesson_unauthenticated():
    response = client.post("/api/v1/bookings/", json={
        "instrument_id": str(uuid.uuid4()),
        "starts_at": datetime.now(timezone.utc).isoformat(),
        "ends_at": datetime.now(timezone.utc).isoformat(),
        "price_cents": 5000,
    })
    assert response.status_code == 401


def test_my_bookings():
    app.dependency_overrides[get_current_user] = lambda: make_mock_user()
    with patch("app.api.bookings.get_student_bookings") as mock:
        mock.return_value = [make_booking_response()]
        response = client.get("/api/v1/bookings/my")
        assert response.status_code == 200
        assert len(response.json()) == 1
    app.dependency_overrides.clear()


def test_list_all_bookings_as_admin():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_user(is_admin=True)
    with patch("app.api.bookings.get_all_bookings") as mock:
        mock.return_value = [make_booking_response()]
        response = client.get("/api/v1/bookings/")
        assert response.status_code == 200
    app.dependency_overrides.clear()


def test_list_all_bookings_not_admin():
    response = client.get("/api/v1/bookings/")
    assert response.status_code == 401


def test_get_booking_by_id_as_admin():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_user(is_admin=True)
    with patch("app.api.bookings.get_booking_by_id") as mock:
        mock.return_value = make_booking_response()
        response = client.get(f"/api/v1/bookings/{uuid.uuid4()}")
        assert response.status_code == 200
    app.dependency_overrides.clear()


def test_get_booking_by_id_not_found():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_user(is_admin=True)
    with patch("app.api.bookings.get_booking_by_id") as mock:
        mock.return_value = None
        response = client.get(f"/api/v1/bookings/{uuid.uuid4()}")
        assert response.status_code == 404
    app.dependency_overrides.clear()


def test_cancel_booking_success():
    app.dependency_overrides[get_current_user] = lambda: make_mock_user()
    with patch("app.api.bookings.cancel_booking") as mock:
        mock.return_value = {**make_booking_response(), "status": "cancelled"}
        response = client.patch(f"/api/v1/bookings/{uuid.uuid4()}/cancel")
        assert response.status_code == 200
    app.dependency_overrides.clear()


def test_cancel_booking_not_found():
    app.dependency_overrides[get_current_user] = lambda: make_mock_user()
    with patch("app.api.bookings.cancel_booking") as mock:
        mock.return_value = None
        response = client.patch(f"/api/v1/bookings/{uuid.uuid4()}/cancel")
        assert response.status_code == 404
    app.dependency_overrides.clear()