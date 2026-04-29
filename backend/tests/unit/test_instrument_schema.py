import uuid
from app.schemas.instrument import InstrumentCreate, InstrumentResponse


def test_instrument_create_valid():
    schema = InstrumentCreate(name="Cello", slug="cello")
    assert schema.name == "Cello"
    assert schema.slug == "cello"


def test_instrument_response_valid():
    schema = InstrumentResponse(
        id=uuid.uuid4(),
        name="Cello",
        slug="cello",
    )
    assert schema.name == "Cello"
    assert schema.slug == "cello"
    assert isinstance(schema.id, uuid.UUID)


def test_instrument_response_from_orm():
    """InstrumentResponse should work with SQLAlchemy model."""
    from app.models.instrument import Instrument
    instrument = Instrument(name="Piano", slug="piano")
    instrument.id = uuid.uuid4()
    schema = InstrumentResponse.model_validate(instrument)
    assert schema.name == "Piano"
    assert schema.slug == "piano"


def test_instrument_create_requires_name():
    from pydantic import ValidationError
    import pytest
    with pytest.raises(ValidationError):
        InstrumentCreate(slug="cello")


def test_instrument_create_requires_slug():
    from pydantic import ValidationError
    import pytest
    with pytest.raises(ValidationError):
        InstrumentCreate(name="Cello")