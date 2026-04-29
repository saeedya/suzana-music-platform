import uuid
from datetime import datetime, timezone
from pydantic import ValidationError
import pytest
from app.schemas.user import UserCreate, UserResponse


def test_user_create_valid():
    schema = UserCreate(
        email="student@example.com",
        full_name="John Doe",
        password="securepassword123",
    )
    assert schema.email == "student@example.com"
    assert schema.full_name == "John Doe"
    assert schema.password == "securepassword123"


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="not-an-email",
            full_name="John Doe",
            password="securepassword123",
        )


def test_user_create_requires_password():
    with pytest.raises(ValidationError):
        UserCreate(
            email="student@example.com",
            full_name="John Doe",
        )


def test_user_response_valid():
    schema = UserResponse(
        id=uuid.uuid4(),
        email="student@example.com",
        full_name="John Doe",
        is_active=True,
        is_admin=False,
        created_at=datetime.now(timezone.utc),
    )
    assert schema.email == "student@example.com"
    assert schema.is_active is True
    assert schema.is_admin is False


def test_user_response_from_orm():
    from app.models.user import User
    user = User(
        email="student@example.com",
        full_name="John Doe",
        hashed_password="hashed",
    )
    user.id = uuid.uuid4()
    user.is_active = True
    user.is_admin = False
    user.created_at = datetime.now(timezone.utc)
    schema = UserResponse.model_validate(user)
    assert schema.email == "student@example.com"
    assert schema.full_name == "John Doe"