import uuid

from app.models.course import Course
from app.models.instrument import Instrument


def make_instrument(db) -> Instrument:
    instrument = Instrument(
        name=f"Test-{uuid.uuid4()}",
        slug=f"test-{uuid.uuid4()}",
    )
    db.add(instrument)
    db.flush()
    return instrument


def make_course(db, instrument_id: uuid.UUID) -> Course:
    course = Course(
        instrument_id=instrument_id,
        title="Cello for Beginners",
        slug=f"cello-{uuid.uuid4()}",
        price_cents=4900,
        level="beginner",
        is_published=True,
        is_active=True,
    )
    db.add(course)
    db.flush()
    return course


def test_get_course_by_id_found(db):
    instrument = make_instrument(db)
    course = make_course(db, instrument.id)

    result = db.query(Course).filter(
        Course.id == course.id,
        Course.is_active == True,  # noqa: E712
    ).first()

    assert result is not None
    assert result.id == course.id


def test_get_course_by_id_not_found(db):
    result = db.query(Course).filter(
        Course.id == uuid.uuid4(),
        Course.is_active == True,  # noqa: E712
    ).first()

    assert result is None


def test_inactive_course_not_returned(db):
    instrument = make_instrument(db)
    course = make_course(db, instrument.id)
    course.is_active = False
    db.flush()

    result = db.query(Course).filter(
        Course.id == course.id,
        Course.is_active == True,  # noqa: E712
    ).first()

    assert result is None