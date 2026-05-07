from datetime import date, time
from unittest.mock import MagicMock

from app.schemas.availability import AvailabilityCreate
from app.services.availability_service import (
    create_availability,
    get_availability,
    get_available_slots,
)


def test_create_availability():
    db = MagicMock()
    data = AvailabilityCreate(
        day_of_week=0,
        start_time=time(9, 0),
        end_time=time(17, 0),
        session_duration=60,
        timezone="America/New_York",
    )
    result = create_availability(db, data)
    db.add.assert_called_once()
    db.commit.assert_called_once()


def test_get_availability():
    db = MagicMock()
    get_availability(db)
    db.query.assert_called_once()


def test_get_available_slots_no_availability():
    db = MagicMock()
    db.query.return_value.filter.return_value.all.return_value = []
    slots = get_available_slots(db, date(2026, 5, 11), 60)
    assert slots == []


def test_get_available_slots_with_availability():
    from app.models.availability import Availability

    db = MagicMock()
    avail = MagicMock(spec=Availability)
    avail.day_of_week = 0
    avail.start_time = time(9, 0)
    avail.end_time = time(11, 0)
    avail.session_duration = 60
    avail.timezone = "America/New_York"

    db.query.return_value.filter.return_value.all.return_value = [avail]
    db.query.return_value.filter.return_value.first.return_value = None

    slots = get_available_slots(db, date(2026, 5, 11), 60)
    assert len(slots) == 2
    assert slots[0].local_time == "09:00"
    assert slots[1].local_time == "10:00"


def test_get_available_slots_booked():
    from app.models.availability import Availability

    db = MagicMock()
    avail = MagicMock(spec=Availability)
    avail.day_of_week = 0
    avail.start_time = time(9, 0)
    avail.end_time = time(10, 0)
    avail.session_duration = 60
    avail.timezone = "America/New_York"

    db.query.return_value.filter.return_value.all.return_value = [avail]
    db.query.return_value.filter.return_value.first.return_value = MagicMock()

    slots = get_available_slots(db, date(2026, 5, 11), 60)
    assert len(slots) == 0


def test_validate_day_of_week():
    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        AvailabilityCreate(
            day_of_week=7,
            start_time=time(9, 0),
            end_time=time(17, 0),
            session_duration=60,
        )


def test_validate_session_duration():
    from pydantic import ValidationError
    import pytest

    with pytest.raises(ValidationError):
        AvailabilityCreate(
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(17, 0),
            session_duration=45,
        )