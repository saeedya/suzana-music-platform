from unittest.mock import patch
from app.core.database import get_db, Base


def test_get_db_yields_session():
    """get_db yields a database session and closes it after use."""
    gen = get_db()
    with patch("app.core.database.SessionLocal") as mock_session:
        mock_db = mock_session.return_value
        gen = get_db()
        db = next(gen)
        assert db == mock_db
        try:
            next(gen)
        except StopIteration:
            pass
        mock_db.close.assert_called_once()


def test_base_is_declarative():
    """Base is a SQLAlchemy DeclarativeBase."""
    assert hasattr(Base, "metadata")
    assert hasattr(Base, "registry")