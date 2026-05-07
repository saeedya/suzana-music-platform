import uuid
from datetime import time

from pydantic import BaseModel, field_validator


class AvailabilityCreate(BaseModel):
    day_of_week: int  # 0=Monday, 6=Sunday
    start_time: time
    end_time: time
    session_duration: int  # 30 or 60
    timezone: str = "America/New_York"

    @field_validator("day_of_week")
    @classmethod
    def validate_day(cls, v: int) -> int:
        if v < 0 or v > 6:
            raise ValueError("day_of_week must be between 0 and 6")
        return v

    @field_validator("session_duration")
    @classmethod
    def validate_duration(cls, v: int) -> int:
        if v not in [30, 60]:
            raise ValueError("session_duration must be 30 or 60")
        return v

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: time, info: object) -> time:
        return v


class AvailabilityResponse(BaseModel):
    id: uuid.UUID
    day_of_week: int
    start_time: time
    end_time: time
    session_duration: int
    is_active: bool
    timezone: str

    model_config = {"from_attributes": True}


class SlotResponse(BaseModel):
    starts_at: str  # ISO datetime UTC
    ends_at: str    # ISO datetime UTC
    local_time: str  # human readable