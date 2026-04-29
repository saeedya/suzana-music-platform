from unittest.mock import patch
from app.core.logging import setup_logging


def test_setup_logging_development():
    """In development, logger should use DEBUG level."""
    with patch("app.core.logging.settings") as mock_settings:
        mock_settings.app_env = "development"
        with patch("app.core.logging.logger") as mock_logger:
            setup_logging()
            mock_logger.remove.assert_called_once()
            call_kwargs = mock_logger.add.call_args[1]
            assert call_kwargs["level"] == "DEBUG"


def test_setup_logging_production():
    """In production, logger should use JSON format."""
    with patch("app.core.logging.settings") as mock_settings:
        mock_settings.app_env = "production"
        with patch("app.core.logging.logger") as mock_logger:
            setup_logging()
            mock_logger.remove.assert_called_once()
            call_kwargs = mock_logger.add.call_args[1]
            assert call_kwargs["serialize"] is True
            assert call_kwargs["level"] == "INFO"