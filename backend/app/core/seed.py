from sqlalchemy.orm import Session

from app.models.instrument import Instrument

INSTRUMENTS = [
    {"name": "Cello", "slug": "cello"},
    {"name": "Piano", "slug": "piano"},
    {"name": "Guitar", "slug": "guitar"},
    {"name": "Music Theory", "slug": "music-theory"},
]


def seed_instruments(db: Session) -> None:
    for item in INSTRUMENTS:
        exists = db.query(Instrument).filter(
            Instrument.slug == item["slug"]
        ).first()
        if not exists:
            db.add(Instrument(name=item["name"], slug=item["slug"]))
    db.commit()


if __name__ == "__main__":  # pragma: no cover
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        seed_instruments(db)
        print("Instruments seeded successfully.")
    finally:
        db.close()