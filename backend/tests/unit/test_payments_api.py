import uuid
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user, get_db
from app.main import app

client = TestClient(app)


def make_mock_user() -> MagicMock:
    user = MagicMock()
    user.id = uuid.uuid4()
    user.is_active = True
    user.is_admin = False
    return user


def test_create_payment_intent_success():
    mock_user = make_mock_user()
    mock_booking = MagicMock()
    mock_booking.id = uuid.uuid4()
    mock_booking.student_id = mock_user.id
    mock_booking.status = "pending"
    mock_booking.price_cents = 5000
    mock_booking.stripe_payment_intent_id = None

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_booking

    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db

    with patch("app.api.payments.create_payment_intent") as mock_intent:
        mock_intent.return_value = MagicMock(id="pi_123", client_secret="secret_123")
        response = client.post("/api/v1/payments/create-intent", json={
            "booking_id": str(uuid.uuid4()),
        })

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert "client_secret" in response.json()


def test_create_payment_intent_unauthenticated():
    response = client.post("/api/v1/payments/create-intent", json={
        "booking_id": str(uuid.uuid4()),
    })
    assert response.status_code == 401


def test_webhook_invalid_signature():
    response = client.post(
        "/api/v1/payments/webhook",
        content=b"payload",
        headers={"stripe-signature": "invalid"},
    )
    assert response.status_code == 400

def test_create_payment_intent_booking_not_found():
    mock_user = make_mock_user()
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post("/api/v1/payments/create-intent", json={
        "booking_id": str(uuid.uuid4()),
    })
    app.dependency_overrides.clear()
    assert response.status_code == 404


def test_create_payment_intent_booking_not_pending():
    mock_user = make_mock_user()
    mock_booking = MagicMock()
    mock_booking.status = "confirmed"

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_booking

    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db

    response = client.post("/api/v1/payments/create-intent", json={
        "booking_id": str(uuid.uuid4()),
    })
    app.dependency_overrides.clear()
    assert response.status_code == 400


def test_webhook_payment_succeeded():
    mock_db = MagicMock()
    mock_booking = MagicMock()
    mock_booking.status = "pending"
    mock_booking.ends_at = MagicMock()
    mock_booking.ends_at.timestamp.return_value = 1234567890.0
    mock_db.query.return_value.filter.return_value.first.return_value = mock_booking

    app.dependency_overrides[get_db] = lambda: mock_db

    with patch("app.api.payments.construct_webhook_event") as mock_event, \
         patch("app.api.payments.create_room") as mock_room:
        mock_event.return_value = MagicMock(
            type="payment_intent.succeeded",
            data=MagicMock(object=MagicMock(id="pi_123"))
        )
        mock_room.return_value = "https://suzana-music.daily.co/booking-123"
        response = client.post(
            "/api/v1/payments/webhook",
            content=b"payload",
            headers={"stripe-signature": "valid"},
        )

    app.dependency_overrides.clear()
    assert response.status_code == 200
    assert mock_booking.status == "confirmed"
    assert mock_booking.daily_room_url == "https://suzana-music.daily.co/booking-123"