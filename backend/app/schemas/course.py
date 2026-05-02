import uuid
from datetime import datetime

from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    price_cents: int
    level: str = "all"
    lesson_count: int | None = None
    is_published: bool = False


class CourseCreate(CourseBase):
    instrument_id: uuid.UUID
    stripe_price_id: str | None = None


class CourseResponse(CourseBase):
    id: uuid.UUID
    instrument_id: uuid.UUID
    stripe_price_id: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price_cents: int | None = None
    level: str | None = None
    lesson_count: int | None = None
    is_published: bool | None = None
    stripe_price_id: str | None = None