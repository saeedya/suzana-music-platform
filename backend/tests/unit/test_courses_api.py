import uuid
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_admin_user
from app.models.user import User

client = TestClient(app)

def make_mock_admin() -> User:
    user = MagicMock(spec=User)
    user.is_admin = True
    user.is_active = True
    return user

def make_course_response(title: str = "Cello for Beginners", slug: str = "cello-for-beginners") -> dict:
    from datetime import datetime, timezone
    return {
        "id": str(uuid.uuid4()),
        "instrument_id": str(uuid.uuid4()),
        "title": title,
        "slug": slug,
        "description": None,
        "price_cents": 4900,
        "level": "all",
        "lesson_count": None,
        "is_published": True,
        "is_active": True,
        "stripe_price_id": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def test_list_courses_returns_200():
    with patch("app.api.courses.get_all_courses") as mock:
        mock.return_value = [make_course_response()]
        response = client.get("/api/v1/courses/")
        assert response.status_code == 200
        assert len(response.json()) == 1


def test_list_courses_empty():
    with patch("app.api.courses.get_all_courses") as mock:
        mock.return_value = []
        response = client.get("/api/v1/courses/")
        assert response.status_code == 200
        assert response.json() == []


def test_get_course_by_slug_found():
    with patch("app.api.courses.get_course_by_slug") as mock:
        mock.return_value = make_course_response()
        response = client.get("/api/v1/courses/cello-for-beginners")
        assert response.status_code == 200
        assert response.json()["slug"] == "cello-for-beginners"


def test_get_course_by_slug_not_found():
    with patch("app.api.courses.get_course_by_slug") as mock:
        mock.return_value = None
        response = client.get("/api/v1/courses/unknown")
        assert response.status_code == 404


def test_list_courses_by_instrument():
    with patch("app.api.courses.get_courses_by_instrument") as mock:
        mock.return_value = [make_course_response()]
        instrument_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/courses/instrument/{instrument_id}")
        assert response.status_code == 200
        assert len(response.json()) == 1

def test_create_course_without_auth_returns_401():
    response = client.post("/api/v1/courses/", json={
        "instrument_id": str(uuid.uuid4()),
        "title": "New Course",
        "slug": "new-course",
        "price_cents": 4900,
    })
    assert response.status_code == 401


def test_update_course_not_found():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_admin()
    with patch("app.api.courses.update_course") as mock:
        mock.return_value = None
        response = client.patch("/api/v1/courses/unknown", json={"price_cents": 5900})
        assert response.status_code == 404
    app.dependency_overrides.clear()


def test_delete_course_not_found():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_admin()
    with patch("app.api.courses.delete_course") as mock:
        mock.return_value = False
        response = client.delete("/api/v1/courses/unknown")
        assert response.status_code == 404
    app.dependency_overrides.clear()

def test_create_course_as_admin():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_admin()
    with patch("app.api.courses.create_course") as mock:
        mock.return_value = make_course_response()
        response = client.post("/api/v1/courses/", json={
            "instrument_id": str(uuid.uuid4()),
            "title": "New Course",
            "slug": "new-course",
            "price_cents": 4900,
        })
        assert response.status_code == 200
    app.dependency_overrides.clear()

def test_update_course_as_admin():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_admin()
    with patch("app.api.courses.update_course") as mock:
        mock.return_value = make_course_response()
        response = client.patch("/api/v1/courses/cello-for-beginners", json={"price_cents": 5900})
        assert response.status_code == 200
    app.dependency_overrides.clear()


def test_delete_course_as_admin():
    app.dependency_overrides[get_admin_user] = lambda: make_mock_admin()
    with patch("app.api.courses.delete_course") as mock:
        mock.return_value = True
        response = client.delete("/api/v1/courses/cello-for-beginners")
        assert response.status_code == 200
        assert response.json()["message"] == "Course deleted successfully"
    app.dependency_overrides.clear()