import uuid
from datetime import datetime

from app.models.user import User


def test_user_tablename():
    assert User.__tablename__ == "users"


def test_user_has_required_fields():
    user = User(
        email="suzana@example.com",
        hashed_password="hashed",
        full_name="Suzana",
    )
    assert user.email == "suzana@example.com"
    assert user.hashed_password == "hashed"
    assert user.full_name == "Suzana"


def test_user_email_is_unique():
    col = User.__table__.c["email"]
    assert col.unique is True


def test_user_email_not_nullable():
    col = User.__table__.c["email"]
    assert col.nullable is False


def test_user_is_active_default():
    col = User.__table__.c["is_active"]
    assert col.default.arg is True


def test_user_is_admin_default():
    col = User.__table__.c["is_admin"]
    assert col.default.arg is False


def test_user_created_at_has_default():
    col = User.__table__.c["created_at"]
    assert col.default is not None