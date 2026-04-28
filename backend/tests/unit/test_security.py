from datetime import timedelta

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_returns_hash():
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"
    assert len(hashed) > 0


def test_verify_password_correct():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token_returns_string():
    token = create_access_token(subject="user-123")
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_access_token_returns_subject():
    token = create_access_token(subject="user-123")
    subject = decode_access_token(token)
    assert subject == "user-123"


def test_decode_access_token_invalid_returns_none():
    subject = decode_access_token("invalid.token.here")
    assert subject is None


def test_decode_access_token_expired():
    token = create_access_token(subject="user-123", expires_delta=timedelta(seconds=-1))
    subject = decode_access_token(token)
    assert subject is None