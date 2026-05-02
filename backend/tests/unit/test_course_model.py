import uuid
from datetime import datetime

from app.models.course import Course


def test_course_tablename():
    assert Course.__tablename__ == "courses"


def test_course_has_required_fields():
    course = Course(
        instrument_id=uuid.uuid4(),
        title="Cello for Beginners",
        slug="cello-for-beginners",
        price_cents=4900,
    )
    assert course.title == "Cello for Beginners"
    assert course.slug == "cello-for-beginners"
    assert course.price_cents == 4900


def test_course_slug_is_unique():
    col = Course.__table__.c["slug"]
    assert col.unique is True


def test_course_title_not_nullable():
    col = Course.__table__.c["title"]
    assert col.nullable is False


def test_course_is_published_default():
    col = Course.__table__.c["is_published"]
    assert col.default.arg is False


def test_course_level_default():
    col = Course.__table__.c["level"]
    assert col.default.arg == "all"


def test_course_description_nullable():
    col = Course.__table__.c["description"]
    assert col.nullable is True


def test_course_created_at_has_default():
    col = Course.__table__.c["created_at"]
    assert col.default is not None