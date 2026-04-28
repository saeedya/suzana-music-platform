import pytest
from pydantic import ValidationError


def test_settings_requires_secret_key():
    """secret_key is required — app must not start without it."""
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class TestSettings(BaseSettings):
        model_config = SettingsConfigDict(env_file=None)
        secret_key: str
        database_url: str

    with pytest.raises(ValidationError):
        TestSettings()


def test_settings_requires_database_url():
    """database_url is required — app must not start without it."""
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class TestSettings(BaseSettings):
        model_config = SettingsConfigDict(env_file=None)
        secret_key: str
        database_url: str

    with pytest.raises(ValidationError):
        TestSettings()


def test_settings_app_env_default(monkeypatch):
    """app_env defaults to development."""
    from pydantic_settings import BaseSettings, SettingsConfigDict

    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

    class TestSettings(BaseSettings):
        model_config = SettingsConfigDict(env_file=None)
        app_env: str = "development"
        secret_key: str
        database_url: str

    s = TestSettings()
    assert s.app_env == "development"


def test_settings_reads_from_env(monkeypatch):
    """Settings correctly reads values from environment."""
    monkeypatch.setenv("SECRET_KEY", "my-secret")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    monkeypatch.setenv("APP_ENV", "production")

    from pydantic_settings import BaseSettings, SettingsConfigDict

    class TestSettings(BaseSettings):
        model_config = SettingsConfigDict(env_file=None)
        app_env: str = "development"
        secret_key: str
        database_url: str

    s = TestSettings()
    assert s.secret_key == "my-secret"
    assert s.database_url == "postgresql://localhost/test"
    assert s.app_env == "production"