from sqlalchemy.orm import Session

from app.models.instrument import Instrument
from app.schemas.instrument import InstrumentCreate, InstrumentResponse


def get_all_instruments(db: Session) -> list[InstrumentResponse]:
    instruments = db.query(Instrument).all()
    return [InstrumentResponse.model_validate(i) for i in instruments]


def get_instrument_by_slug(db: Session, slug: str) -> InstrumentResponse | None:
    instrument = db.query(Instrument).filter(Instrument.slug == slug).first()
    if not instrument:
        return None
    return InstrumentResponse.model_validate(instrument)


def create_instrument(db: Session, data: InstrumentCreate) -> InstrumentResponse:
    instrument = Instrument(name=data.name, slug=data.slug)
    db.add(instrument)
    db.commit()
    db.refresh(instrument)
    return InstrumentResponse.model_validate(instrument)