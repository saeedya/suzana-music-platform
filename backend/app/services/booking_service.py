from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse


def create_booking(
    db: Session, data: BookingCreate, student_id: str
) -> BookingResponse:
    booking = Booking(
        student_id=student_id,
        instrument_id=data.instrument_id,
        starts_at=data.starts_at,
        ends_at=data.ends_at,
        price_cents=data.price_cents,
        notes=data.notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return BookingResponse.model_validate(booking)


def get_student_bookings(
    db: Session, student_id: str
) -> list[BookingResponse]:
    bookings = db.query(Booking).filter(
        Booking.student_id == student_id
    ).all()
    return [BookingResponse.model_validate(b) for b in bookings]


def get_all_bookings(db: Session) -> list[BookingResponse]:
    bookings = db.query(Booking).all()
    return [BookingResponse.model_validate(b) for b in bookings]


def cancel_booking(
    db: Session, booking_id: str, student_id: str
) -> BookingResponse | None:
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.student_id == student_id,
    ).first()
    if not booking:
        return None
    if booking.status not in ("pending", "confirmed"):
        return None
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return BookingResponse.model_validate(booking)


def get_booking_by_id(
    db: Session, booking_id: str
) -> BookingResponse | None:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        return None
    return BookingResponse.model_validate(booking)