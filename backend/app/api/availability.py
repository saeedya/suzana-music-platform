from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_admin_user, get_current_user
from app.models.availability import Availability
from app.models.user import User
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityResponse,
    SlotResponse,
)
from app.services.availability_service import (
    create_availability,
    get_availability,
    get_available_slots,
)

router = APIRouter(prefix="/api/v1/availability", tags=["availability"])


@router.post("/", response_model=AvailabilityResponse)
def create(
    data: AvailabilityCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> Availability:
    return create_availability(db, data)


@router.get("/", response_model=list[AvailabilityResponse])
def list_availability(
    db: Session = Depends(get_db),
) -> list[Availability]:
    return get_availability(db)


@router.get("/slots", response_model=list[SlotResponse])
def get_slots(
    target_date: date,
    session_duration: int = 60,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[SlotResponse]:
    if session_duration not in [30, 60]:
        raise HTTPException(status_code=400, detail="session_duration must be 30 or 60")
    return get_available_slots(db, target_date, session_duration)