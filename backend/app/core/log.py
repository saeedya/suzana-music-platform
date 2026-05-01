import sys

from loguru import logger

from app.core.config import settings


def setup_logging() -> None:
    logger.remove()

    if settings.app_env == "production":
        logger.add(
            sys.stdout,
            format="{time} {level} {message}",
            level="INFO",
            serialize=True,  # JSON format
        )
    else:
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> \
                | <cyan>{name}</cyan> - <level>{message}</level>",
            level="DEBUG",
            colorize=True,
        )