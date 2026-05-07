from datetime import time
import uuid

from app.models.availability import Availability
from app.services.availability_service import (
    get_availability,
    get_available_slots,
    create_availability,
)
from app.schemas.availability import AvailabilityCreate


def make_availability(db, day_of_week=0, start="09:00", end="11:00", duration=60):
    avail = Availability(
        id=uuid.uuid4(),
        day_of_week=day_of_week,
        start_time=time(int(start.split(":")[0]), int(start.split(":")[1])),
        end_time=time(int(end.split(":")[0]), int(end.split(":")[1])),
        session_duration=duration,
        is_active=True,
        timezone="America/New_York",
    )
    db.add(avail)
    db.flush()
    return avail


def test_create_availability_in_db(db):
    data = AvailabilityCreate(
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
        session_duration=60,
        timezone="America/New_York",
    )
    result = create_availability(db, data)
    assert result.id is not None
    assert result.day_of_week == 0
    assert result.session_duration == 60


def test_get_availability_from_db(db):
    make_availability(db)
    results = get_availability(db)
    assert len(results) >= 1


def test_get_available_slots_from_db(db):
    from datetime import date
    make_availability(db, day_of_week=0, start="09:00", end="11:00", duration=60)
    # May 11 2026 is a Monday
    slots = get_available_slots(db, date(2026, 5, 11), 60)
    assert len(slots) >= 2
    local_times = [s.local_time for s in slots]
    assert "09:00" in local_times
    assert "10:00" in local_times


def test_get_available_slots_wrong_day(db):
    from datetime import date
    make_availability(db, day_of_week=0)  # Monday
    # May 12 2026 is a Tuesday
    slots = get_available_slots(db, date(2026, 5, 12), 60)
    assert slots == []