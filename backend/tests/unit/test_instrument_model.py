import uuid

from app.models.instrument import Instrument


def test_instrument_tablename():
    assert Instrument.__tablename__ == "instruments"


def test_instrument_has_id():
    instrument = Instrument(name="Cello", slug="cello")
    assert instrument.id is None or isinstance(instrument.id, uuid.UUID)


def test_instrument_has_name():
    instrument = Instrument(name="Cello", slug="cello")
    assert instrument.name == "Cello"


def test_instrument_has_slug():
    instrument = Instrument(name="Cello", slug="cello")
    assert instrument.slug == "cello"


def test_instrument_slug_is_unique_constraint():
    col = Instrument.__table__.c["slug"]
    assert col.unique is True


def test_instrument_name_not_nullable():
    col = Instrument.__table__.c["name"]
    assert col.nullable is False