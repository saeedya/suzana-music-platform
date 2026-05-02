import uuid
from datetime import datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    instrument_id: uuid.UUID
    starts_at: datetime
    ends_at: datetime
    price_cents: int
    notes: str | None = None


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: uuid.UUID
    student_id: uuid.UUID
    status: str
    stripe_payment_intent_id: str | None = None
    daily_room_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class BookingStatusUpdate(BaseModel):
    status: str