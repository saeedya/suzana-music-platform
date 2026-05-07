import uuid
from datetime import time

from sqlalchemy import Boolean, Integer, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Availability(Base):
    __tablename__ = "availability"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    day_of_week: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # 0=Monday, 6=Sunday
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    session_duration: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # minutes: 30 or 60
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    timezone: Mapped[str] = mapped_column(
        String, nullable=False, default="America/New_York"
    )