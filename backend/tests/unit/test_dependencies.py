import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.dependencies import get_current_user, get_admin_user
from app.models.user import User


def make_mock_user(is_active: bool = True, is_admin: bool = False) -> User:
    user = MagicMock(spec=User)
    user.email = "test@example.com"
    user.is_active = is_active
    user.is_admin = is_admin
    return user


def make_credentials(token: str = "valid-token") -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_get_current_user_success():
    db = MagicMock()
    mock_user = make_mock_user()
    db.query.return_value.filter.return_value.first.return_value = mock_user

    with patch("app.core.dependencies.supabase") as mock_supabase:
        mock_supabase.auth.get_user.return_value.user = MagicMock(
            email="test@example.com"
        )
        result = get_current_user(make_credentials(), db)
        assert result == mock_user


def test_get_current_user_invalid_token():
    db = MagicMock()

    with patch("app.core.dependencies.supabase") as mock_supabase:
        mock_supabase.auth.get_user.return_value.user = None
        with pytest.raises(HTTPException) as exc:
            get_current_user(make_credentials("invalid"), db)
        assert exc.value.status_code == 401


def test_get_current_user_not_in_db():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    with patch("app.core.dependencies.supabase") as mock_supabase:
        mock_supabase.auth.get_user.return_value.user = MagicMock(
            email="test@example.com"
        )
        with pytest.raises(HTTPException) as exc:
            get_current_user(make_credentials(), db)
        assert exc.value.status_code == 401


def test_get_current_user_inactive():
    db = MagicMock()
    mock_user = make_mock_user(is_active=False)
    db.query.return_value.filter.return_value.first.return_value = mock_user

    with patch("app.core.dependencies.supabase") as mock_supabase:
        mock_supabase.auth.get_user.return_value.user = MagicMock(
            email="test@example.com"
        )
        with pytest.raises(HTTPException) as exc:
            get_current_user(make_credentials(), db)
        assert exc.value.status_code == 403


def test_get_admin_user_success():
    mock_user = make_mock_user(is_admin=True)
    result = get_admin_user(mock_user)
    assert result == mock_user


def test_get_admin_user_not_admin():
    mock_user = make_mock_user(is_admin=False)
    with pytest.raises(HTTPException) as exc:
        get_admin_user(mock_user)
    assert exc.value.status_code == 403