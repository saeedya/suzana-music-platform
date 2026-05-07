from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.availability import Availability
from app.models.booking import Booking
from app.schemas.availability import AvailabilityCreate, SlotResponse


def create_availability(db: Session, data: AvailabilityCreate) -> Availability:
    availability = Availability(
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
        session_duration=data.session_duration,
        timezone=data.timezone,
    )
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


def get_availability(db: Session) -> list[Availability]:
    return db.query(Availability).filter(Availability.is_active == True).all()  # noqa: E712


def get_available_slots(
    db: Session,
    target_date: date,
    session_duration: int,
) -> list[SlotResponse]:
    # Get day of week (0=Monday)
    day_of_week = target_date.weekday()

    # Get availability for this day
    availabilities = (
        db.query(Availability)
        .filter(
            Availability.day_of_week == day_of_week,
            Availability.is_active == True,  # noqa: E712
            Availability.session_duration == session_duration,
        )
        .all()
    )

    if not availabilities:
        return []

    slots = []

    for avail in availabilities:
        tz = ZoneInfo(avail.timezone)

        # Build datetime objects in Suzana's timezone
        current = datetime.combine(target_date, avail.start_time, tzinfo=tz)
        end = datetime.combine(target_date, avail.end_time, tzinfo=tz)

        while current + timedelta(minutes=session_duration) <= end:
            slot_end = current + timedelta(minutes=session_duration)

            # Check if slot is already booked
            starts_at_utc = current.astimezone(timezone.utc)
            ends_at_utc = slot_end.astimezone(timezone.utc)

            existing = (
                db.query(Booking)
                .filter(
                    Booking.starts_at < ends_at_utc,
                    Booking.ends_at > starts_at_utc,
                    Booking.status.in_(["pending", "confirmed"]),
                )
                .first()
            )

            if not existing:
                slots.append(
                    SlotResponse(
                        starts_at=starts_at_utc.isoformat(),
                        ends_at=ends_at_utc.isoformat(),
                        local_time=current.strftime("%H:%M"),
                    )
                )

            current += timedelta(minutes=session_duration)

    return slots