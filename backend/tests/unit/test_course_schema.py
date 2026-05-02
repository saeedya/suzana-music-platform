import uuid
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate


def test_course_create_valid():
    schema = CourseCreate(
        instrument_id=uuid.uuid4(),
        title="Cello for Beginners",
        slug="cello-for-beginners",
        price_cents=4900,
    )
    assert schema.title == "Cello for Beginners"
    assert schema.level == "all"
    assert schema.is_published is False


def test_course_create_requires_title():
    with pytest.raises(ValidationError):
        CourseCreate(
            instrument_id=uuid.uuid4(),
            slug="cello-for-beginners",
            price_cents=4900,
        )


def test_course_create_requires_price():
    with pytest.raises(ValidationError):
        CourseCreate(
            instrument_id=uuid.uuid4(),
            title="Cello for Beginners",
            slug="cello-for-beginners",
        )


def test_course_response_from_orm():
    from app.models.course import Course
    course = Course(
        instrument_id=uuid.uuid4(),
        title="Cello for Beginners",
        slug="cello-for-beginners",
        price_cents=4900,
        level="all",
        is_published=False,
    )
    course.id = uuid.uuid4()
    course.created_at = datetime.now(timezone.utc)
    schema = CourseResponse.model_validate(course)
    assert schema.title == "Cello for Beginners"
    assert schema.price_cents == 4900


def test_course_update_partial():
    update = CourseUpdate(price_cents=5900)
    data = update.model_dump(exclude_unset=True)
    assert "price_cents" in data
    assert "title" not in data