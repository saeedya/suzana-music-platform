from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_admin_user, get_current_user
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import (
    cancel_booking,
    create_booking,
    get_all_bookings,
    get_booking_by_id,
    get_student_bookings,
)

router = APIRouter(prefix="/api/v1/bookings", tags=["bookings"])


@router.post("/", response_model=BookingResponse)
def book_lesson(
    data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BookingResponse:
    return create_booking(db, data, str(current_user.id))


@router.get("/my", response_model=list[BookingResponse])
def my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[BookingResponse]:
    return get_student_bookings(db, str(current_user.id))


@router.get("/", response_model=list[BookingResponse])
def list_all_bookings(
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> list[BookingResponse]:
    return get_all_bookings(db)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> BookingResponse:
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_my_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BookingResponse:
    booking = cancel_booking(db, booking_id, str(current_user.id))
    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found or cannot be cancelled",
        )
    return booking