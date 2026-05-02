from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.booking import Booking
from app.models.user import User
from app.services.daily_service import create_room
from app.services.email_service import (
    send_booking_confirmation_student,
    send_booking_confirmation_suzana,
)
from app.services.payment_service import (
    construct_webhook_event,
    create_payment_intent,
)

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])


class CreatePaymentIntentRequest(BaseModel):
    booking_id: str


class CreatePaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str


@router.post("/create-intent", response_model=CreatePaymentIntentResponse)
def create_intent(
    data: CreatePaymentIntentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CreatePaymentIntentResponse:
    booking = db.query(Booking).filter(
        Booking.id == data.booking_id,
        Booking.student_id == current_user.id,
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status != "pending":
        raise HTTPException(status_code=400, detail="Booking is not pending")

    intent = create_payment_intent(
        amount_cents=booking.price_cents,
        currency="usd",
        metadata={"booking_id": str(booking.id)},
    )

    booking.stripe_payment_intent_id = intent.id
    db.commit()

    return CreatePaymentIntentResponse(
        client_secret=intent.client_secret or "",
        payment_intent_id=intent.id,
    )


@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db),
    stripe_signature: str = Header(alias="stripe-signature"),
) -> dict[str, str]:
    payload = await request.body()

    try:
        event = construct_webhook_event(payload, stripe_signature)
    except Exception as err:
        raise HTTPException(
            status_code=400, detail="Invalid webhook signature") from err

    if event.type == "payment_intent.succeeded":
        payment_intent_id = event.data.object.id
        booking = db.query(Booking).filter(
            Booking.stripe_payment_intent_id == payment_intent_id
        ).first()
        if booking:
            booking.status = "confirmed"
            room_url = create_room(
                str(booking.id),
                booking.starts_at.timestamp(),
                booking.ends_at.timestamp(),
            )
            booking.daily_room_url = room_url
            db.commit()

            # Send confirmation emails
            starts_at_str = booking.starts_at.strftime("%A, %B %d %Y at %H:%M UTC")
            ends_at_str = booking.ends_at.strftime("%H:%M UTC")

            send_booking_confirmation_student(
                student_email=booking.student.email,
                student_name=booking.student.full_name,
                instrument=booking.instrument.name,
                starts_at=starts_at_str,
                ends_at=ends_at_str,
                room_url=room_url,
            )

            send_booking_confirmation_suzana(
                suzana_email=settings.teacher_email,
                student_name=booking.student.full_name,
                student_email=booking.student.email,
                instrument=booking.instrument.name,
                starts_at=starts_at_str,
                ends_at=ends_at_str,
                room_url=room_url,
            )

    return {"status": "ok"}