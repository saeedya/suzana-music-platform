from app.core.seed import seed_instruments
from app.models.instrument import Instrument
from app.services.instrument_service import (
    create_instrument,
    get_all_instruments,
    get_instrument_by_slug,
)
from app.schemas.instrument import InstrumentCreate


def test_seed_instruments_inserts_to_db(db):
    seed_instruments(db)
    instruments = db.query(Instrument).all()
    assert len(instruments) == 4
    slugs = [i.slug for i in instruments]
    assert "cello" in slugs
    assert "piano" in slugs
    assert "guitar" in slugs
    assert "music-theory" in slugs


def test_create_instrument_in_db(db):
    data = InstrumentCreate(name="Violin", slug="violin")
    result = create_instrument(db, data)
    assert result.name == "Violin"
    assert result.slug == "violin"


def test_get_instrument_by_slug_from_db(db):
    data = InstrumentCreate(name="Drums", slug="drums")
    create_instrument(db, data)
    result = get_instrument_by_slug(db, "drums")
    assert result is not None
    assert result.name == "Drums"


def test_get_instrument_by_slug_not_found_in_db(db):
    result = get_instrument_by_slug(db, "nonexistent")
    assert result is None


def test_get_all_instruments_from_db(db):
    create_instrument(db, InstrumentCreate(name="Harp", slug="harp"))
    create_instrument(db, InstrumentCreate(name="Flute", slug="flute"))
    results = get_all_instruments(db)
    assert len(results) >= 2