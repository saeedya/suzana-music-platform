from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_admin_user
from app.models.user import User
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate
from app.services.course_service import (
    create_course,
    delete_course,
    get_all_courses,
    get_course_by_id,
    get_course_by_slug,
    get_courses_by_instrument,
    update_course,
)

router = APIRouter(prefix="/api/v1/courses", tags=["courses"])


@router.get("/", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)) -> list[CourseResponse]:
    return get_all_courses(db)


@router.get("/instrument/{instrument_id}", response_model=list[CourseResponse])
def list_courses_by_instrument(
    instrument_id: str, db: Session = Depends(get_db)
) -> list[CourseResponse]:
    return get_courses_by_instrument(db, instrument_id)

@router.get("/id/{course_id}", response_model=CourseResponse)
def get_course_by_id_route(
    course_id: str, db: Session = Depends(get_db)
) -> CourseResponse:
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/{slug}", response_model=CourseResponse)
def get_course(slug: str, db: Session = Depends(get_db)) -> CourseResponse:
    course = get_course_by_slug(db, slug)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/", response_model=CourseResponse)
def create_new_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> CourseResponse:
    return create_course(db, data)


@router.patch("/{slug}", response_model=CourseResponse)
def update_existing_course(
    slug: str,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> CourseResponse:
    course = update_course(db, slug, data)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.delete("/{slug}")
def delete_existing_course(
    slug: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> dict[str, str]:
    success = delete_course(db, slug)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"message": "Course deleted successfully"}