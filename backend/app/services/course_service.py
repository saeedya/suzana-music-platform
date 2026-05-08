from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate


def get_all_courses(db: Session, published_only: bool = True) -> list[CourseResponse]:
    query = db.query(Course).filter(Course.is_active == True)  # noqa: E712
    if published_only:
        query = query.filter(Course.is_published == True)  # noqa: E712
    return [CourseResponse.model_validate(c) for c in query.all()]


def get_courses_by_instrument(
    db: Session, instrument_id: str, published_only: bool = True
) -> list[CourseResponse]:
    query = db.query(Course).filter(
        Course.instrument_id == instrument_id,
        Course.is_active == True,  # noqa: E712
    )
    if published_only:
        query = query.filter(Course.is_published == True)  # noqa: E712
    return [CourseResponse.model_validate(c) for c in query.all()]


def get_course_by_slug(db: Session, slug: str) -> CourseResponse | None:
    course = db.query(Course).filter(
        Course.slug == slug,
        Course.is_active == True,  # noqa: E712
    ).first()
    if not course:
        return None
    return CourseResponse.model_validate(course)

def get_course_by_id(db: Session, course_id: str) -> CourseResponse | None:
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.is_active == True,  # noqa: E712
    ).first()
    if not course:
        return None
    return CourseResponse.model_validate(course)

def create_course(db: Session, data: CourseCreate) -> CourseResponse:
    course = Course(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseResponse.model_validate(course)


def update_course(
    db: Session, slug: str, data: "CourseUpdate"
) -> CourseResponse | None:
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.commit()
    db.refresh(course)
    return CourseResponse.model_validate(course)


def delete_course(db: Session, slug: str) -> bool:
    course = db.query(Course).filter(Course.slug == slug).first()
    if not course:
        return False
    course.is_active = False
    db.commit()
    return True