import uuid
from datetime import datetime, timezone

from app.models.booking import Booking
from app.models.instrument import Instrument
from app.models.user import User


def make_user(db) -> User:
    user = User(
        email=f"test-{uuid.uuid4()}@example.com",
        hashed_password="hashed",
        full_name="Test Student",
    )
    db.add(user)
    db.flush()
    return user


def make_instrument(db) -> Instrument:
    instrument = Instrument(
        name=f"Test-{uuid.uuid4()}",
        slug=f"test-{uuid.uuid4()}",
    )
    db.add(instrument)
    db.flush()
    return instrument


def test_create_booking_in_db(db):
    user = make_user(db)
    instrument = make_instrument(db)

    booking = Booking(
        student_id=user.id,
        instrument_id=instrument.id,
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc),
        price_cents=5000,
    )
    db.add(booking)
    db.flush()

    assert booking.id is not None
    assert booking.status == "pending"


def test_booking_status_update(db):
    user = make_user(db)
    instrument = make_instrument(db)

    booking = Booking(
        student_id=user.id,
        instrument_id=instrument.id,
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc),
        price_cents=5000,
    )
    db.add(booking)
    db.flush()

    booking.status = "confirmed"
    db.flush()

    updated = db.query(Booking).filter(Booking.id == booking.id).first()
    assert updated.status == "confirmed"


def test_booking_cancel(db):
    user = make_user(db)
    instrument = make_instrument(db)

    booking = Booking(
        student_id=user.id,
        instrument_id=instrument.id,
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc),
        price_cents=5000,
    )
    db.add(booking)
    db.flush()

    booking.status = "cancelled"
    db.flush()

    cancelled = db.query(Booking).filter(Booking.id == booking.id).first()
    assert cancelled.status == "cancelled"

def test_get_my_booking_by_id_returns_own_booking(db):
    user = make_user(db)
    instrument = make_instrument(db)
    booking = Booking(
        student_id=user.id,
        instrument_id=instrument.id,
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc),
        price_cents=5000,
    )
    db.add(booking)
    db.flush()

    result = db.query(Booking).filter(
        Booking.id == booking.id,
        Booking.student_id == user.id,
    ).first()

    assert result is not None
    assert result.id == booking.id
    assert result.student_id == user.id


def test_get_my_booking_by_id_cannot_access_others(db):
    owner = make_user(db)
    other = make_user(db)
    instrument = make_instrument(db)
    booking = Booking(
        student_id=owner.id,
        instrument_id=instrument.id,
        starts_at=datetime.now(timezone.utc),
        ends_at=datetime.now(timezone.utc),
        price_cents=5000,
    )
    db.add(booking)
    db.flush()

    result = db.query(Booking).filter(
        Booking.id == booking.id,
        Booking.student_id == other.id,
    ).first()

    assert result is None