import uuid
from unittest.mock import MagicMock, patch
from app.services.course_service import (
    get_all_courses,
    get_courses_by_instrument,
    get_course_by_slug,
    create_course,
    update_course,
    delete_course,
)
from app.schemas.course import CourseCreate, CourseUpdate


def make_mock_course(title: str = "Cello for Beginners", slug: str = "cello-for-beginners") -> MagicMock:
    course = MagicMock()
    course.id = uuid.uuid4()
    course.instrument_id = uuid.uuid4()
    course.title = title
    course.slug = slug
    course.description = None
    course.price_cents = 4900
    course.level = "all"
    course.lesson_count = None
    course.is_published = True
    course.is_active = True
    course.stripe_price_id = None
    from datetime import datetime, timezone
    course.created_at = datetime.now(timezone.utc)
    return course


def test_get_all_courses_returns_list():
    db = MagicMock()
    db.query.return_value.filter.return_value.filter.return_value.all.return_value = [
        make_mock_course()
    ]
    result = get_all_courses(db)
    assert len(result) == 1


def test_get_all_courses_empty():
    db = MagicMock()
    db.query.return_value.filter.return_value.filter.return_value.all.return_value = []
    result = get_all_courses(db)
    assert result == []


def test_get_course_by_slug_found():
    db = MagicMock()
    mock_course = make_mock_course()
    db.query.return_value.filter.return_value.first.return_value = mock_course
    result = get_course_by_slug(db, "cello-for-beginners")
    assert result is not None
    assert result.slug == "cello-for-beginners"


def test_get_course_by_slug_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    result = get_course_by_slug(db, "unknown")
    assert result is None


def test_create_course():
    db = MagicMock()
    mock_course = make_mock_course()
    with patch("app.services.course_service.Course") as MockCourse:
        MockCourse.return_value = mock_course
        data = CourseCreate(
            instrument_id=uuid.uuid4(),
            title="Cello for Beginners",
            slug="cello-for-beginners",
            price_cents=4900,
        )
        result = create_course(db, data)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        assert result.title == "Cello for Beginners"


def test_update_course_found():
    db = MagicMock()
    mock_course = make_mock_course()
    db.query.return_value.filter.return_value.first.return_value = mock_course
    data = CourseUpdate(price_cents=5900)
    result = update_course(db, "cello-for-beginners", data)
    assert result is not None
    db.commit.assert_called_once()


def test_update_course_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    result = update_course(db, "unknown", CourseUpdate(price_cents=5900))
    assert result is None


def test_delete_course_found():
    db = MagicMock()
    mock_course = make_mock_course()
    db.query.return_value.filter.return_value.first.return_value = mock_course
    result = delete_course(db, "cello-for-beginners")
    assert result is True
    assert mock_course.is_active is False
    db.commit.assert_called_once()


def test_delete_course_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    result = delete_course(db, "unknown")
    assert result is False

def test_get_courses_by_instrument():
    db = MagicMock()
    db.query.return_value.filter.return_value.filter.return_value.all.return_value = [
        make_mock_course()
    ]
    result = get_courses_by_instrument(db, str(uuid.uuid4()))
    assert len(result) == 1


def test_get_courses_by_instrument_empty():
    db = MagicMock()
    db.query.return_value.filter.return_value.filter.return_value.all.return_value = []
    result = get_courses_by_instrument(db, str(uuid.uuid4()))
    assert result == []