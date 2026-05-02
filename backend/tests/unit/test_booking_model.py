import uuid
from datetime import datetime, timezone

from app.models.booking import Booking


def test_booking_tablename():
    assert Booking.__tablename__ == "bookings"


def test_booking_has_required_fields():
    booking = Booking(
        student_id=uuid.uuid4(),
        instrument_id=uuid.uuid4(),
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc),
        price_cents=5000,
    )
    assert booking.price_cents == 5000


def test_booking_status_default():
    col = Booking.__table__.c["status"]
    assert col.default.arg == "pending"


def test_booking_stripe_payment_intent_id_nullable():
    col = Booking.__table__.c["stripe_payment_intent_id"]
    assert col.nullable is True


def test_booking_daily_room_url_nullable():
    col = Booking.__table__.c["daily_room_url"]
    assert col.nullable is True


def test_booking_notes_nullable():
    col = Booking.__table__.c["notes"]
    assert col.nullable is True


def test_booking_created_at_has_default():
    col = Booking.__table__.c["created_at"]
    assert col.default is not None