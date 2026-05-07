import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from app.schemas.booking import BookingCreate
from app.services.booking_service import (
    cancel_booking,
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    get_my_booking_by_id,
    get_student_bookings,
)


def make_mock_booking(status: str = "pending") -> MagicMock:
    booking = MagicMock()
    booking.id = uuid.uuid4()
    booking.student_id = uuid.uuid4()
    booking.instrument_id = uuid.uuid4()
    booking.starts_at = datetime.now(timezone.utc)
    booking.ends_at = datetime.now(timezone.utc)
    booking.status = status
    booking.price_cents = 5000
    booking.notes = None
    booking.stripe_payment_intent_id = None
    booking.daily_room_url = None
    booking.created_at = datetime.now(timezone.utc)
    return booking


def make_booking_create() -> BookingCreate:
    return BookingCreate(
        instrument_id=uuid.uuid4(),
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc),
        price_cents=5000,
    )


def test_create_booking():
    db = MagicMock()
    mock_booking = make_mock_booking()
    with patch("app.services.booking_service.Booking") as MockBooking:
        MockBooking.return_value = mock_booking
        result = create_booking(db, make_booking_create(), str(uuid.uuid4()))
        db.add.assert_called_once()
        db.commit.assert_called_once()
        assert result is not None


def test_get_student_bookings():
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = [
        make_mock_booking()
    ]
    result = get_student_bookings(db, str(uuid.uuid4()))
    assert len(result) == 1


def test_get_student_bookings_empty():
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []
    result = get_student_bookings(db, str(uuid.uuid4()))
    assert result == []


def test_get_all_bookings():
    db = MagicMock()
    db.query.return_value.all.return_value = [
        make_mock_booking(),
        make_mock_booking(),
    ]
    result = get_all_bookings(db)
    assert len(result) == 2


def test_get_booking_by_id_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = make_mock_booking()
    result = get_booking_by_id(db, str(uuid.uuid4()))
    assert result is not None


def test_get_booking_by_id_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    result = get_booking_by_id(db, str(uuid.uuid4()))
    assert result is None


def test_cancel_booking_success():
    db = MagicMock()
    mock_booking = make_mock_booking(status="confirmed")
    mock_booking.starts_at = MagicMock()
    mock_booking.starts_at.strftime.return_value = "Monday, May 01 2026 at 10:00 UTC"
    db.query.return_value.filter.return_value.first.return_value = mock_booking
    with patch("app.services.booking_service.send_booking_cancelled_student") as mock_email:
        result = cancel_booking(db, str(uuid.uuid4()), str(uuid.uuid4()))
        assert result is not None
        assert mock_booking.status == "cancelled"
        db.commit.assert_called_once()
        mock_email.assert_called_once()


def test_cancel_booking_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    result = cancel_booking(db, str(uuid.uuid4()), str(uuid.uuid4()))
    assert result is None


def test_cancel_booking_already_cancelled():
    db = MagicMock()
    mock_booking = make_mock_booking(status="cancelled")
    db.query.return_value.filter.return_value.first.return_value = mock_booking
    result = cancel_booking(db, str(uuid.uuid4()), str(uuid.uuid4()))
    assert result is None


def test_get_my_booking_by_id_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = make_mock_booking()
    result = get_my_booking_by_id(db, str(uuid.uuid4()), str(uuid.uuid4()))
    assert result is not None


def test_get_my_booking_by_id_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    result = get_my_booking_by_id(db, str(uuid.uuid4()), str(uuid.uuid4()))
    assert result is None