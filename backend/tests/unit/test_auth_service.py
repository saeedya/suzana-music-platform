from unittest.mock import MagicMock
from app.services.auth_service import sign_up, sign_in, sign_out, get_user
from app.schemas.user import UserCreate


def make_mock_client() -> MagicMock:
    return MagicMock()


def test_sign_up_returns_user_and_session():
    client = make_mock_client()
    client.auth.sign_up.return_value.user = MagicMock(id="123", email="test@example.com")
    client.auth.sign_up.return_value.session = MagicMock(access_token="token")

    data = UserCreate(email="test@example.com", full_name="Test", password="pass123")
    result = sign_up(client, data)

    assert "user" in result
    assert "session" in result
    client.auth.sign_up.assert_called_once()


def test_sign_in_returns_user_and_session():
    client = make_mock_client()
    client.auth.sign_in_with_password.return_value.user = MagicMock()
    client.auth.sign_in_with_password.return_value.session = MagicMock()

    result = sign_in(client, "test@example.com", "pass123")

    assert "user" in result
    assert "session" in result
    client.auth.sign_in_with_password.assert_called_once()


def test_sign_out_calls_client():
    client = make_mock_client()
    sign_out(client, "some-jwt")
    client.auth.sign_out.assert_called_once()


def test_get_user_returns_user():
    client = make_mock_client()
    client.auth.get_user.return_value.user = MagicMock(
        id="123", email="test@example.com"
    )

    result = get_user(client, "some-jwt")

    assert result is not None
    assert result["email"] == "test@example.com"


def test_get_user_returns_none_when_no_user():
    client = make_mock_client()
    client.auth.get_user.return_value.user = None

    result = get_user(client, "invalid-jwt")

    assert result is None