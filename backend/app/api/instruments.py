from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.instrument import InstrumentResponse
from app.services.instrument_service import get_all_instruments, get_instrument_by_slug

router = APIRouter(prefix="/api/v1/instruments", tags=["instruments"])


@router.get("/", response_model=list[InstrumentResponse])
def list_instruments(db: Session = Depends(get_db)) -> list[InstrumentResponse]:
    return get_all_instruments(db)


@router.get("/{slug}", response_model=InstrumentResponse)
def get_instrument(slug: str, db: Session = Depends(get_db)) -> InstrumentResponse:
    instrument = get_instrument_by_slug(db, slug)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")
    return instrument