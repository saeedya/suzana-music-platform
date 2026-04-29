import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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