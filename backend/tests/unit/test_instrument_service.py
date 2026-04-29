import uuid
from unittest.mock import MagicMock, patch
from app.services.instrument_service import (
    get_all_instruments,
    get_instrument_by_slug,
    create_instrument,
)
from app.schemas.instrument import InstrumentCreate


def make_mock_instrument(name: str, slug: str) -> MagicMock:
    instrument = MagicMock()
    instrument.id = uuid.uuid4()
    instrument.name = name
    instrument.slug = slug
    return instrument


def test_get_all_instruments_returns_list():
    db = MagicMock()
    db.query.return_value.all.return_value = [
        make_mock_instrument("Cello", "cello"),
        make_mock_instrument("Piano", "piano"),
    ]
    result = get_all_instruments(db)
    assert len(result) == 2
    assert result[0].name == "Cello"
    assert result[1].name == "Piano"


def test_get_all_instruments_empty():
    db = MagicMock()
    db.query.return_value.all.return_value = []
    result = get_all_instruments(db)
    assert result == []


def test_get_instrument_by_slug_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = (
        make_mock_instrument("Cello", "cello")
    )
    result = get_instrument_by_slug(db, "cello")
    assert result is not None
    assert result.slug == "cello"


def test_get_instrument_by_slug_not_found():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    result = get_instrument_by_slug(db, "unknown")
    assert result is None


def test_create_instrument():
    db = MagicMock()
    mock_instrument = make_mock_instrument("Guitar", "guitar")
    db.refresh.side_effect = lambda obj: None

    with patch("app.services.instrument_service.Instrument") as MockInstrument:
        MockInstrument.return_value = mock_instrument
        data = InstrumentCreate(name="Guitar", slug="guitar")
        result = create_instrument(db, data)
        db.add.assert_called_once()
        db.commit.assert_called_once()
        assert result.name == "Guitar"