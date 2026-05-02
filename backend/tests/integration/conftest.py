import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import all models explicitly to register with SQLAlchemy
from app.models.instrument import Instrument  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.course import Course  # noqa: F401
from app.models.booking import Booking  # noqa: F401

INTEGRATION_TEST_DB_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:54322/postgres"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(INTEGRATION_TEST_DB_URL)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def db(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()