from unittest.mock import MagicMock, patch
from app.core.seed import seed_instruments, INSTRUMENTS


def test_seed_instruments_adds_all_when_empty():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    seed_instruments(db)

    assert db.add.call_count == len(INSTRUMENTS)
    db.commit.assert_called_once()


def test_seed_instruments_skips_existing():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = MagicMock()

    seed_instruments(db)

    db.add.assert_not_called()
    db.commit.assert_called_once()


def test_seed_instruments_idempotent():
    """Running seed twice should not add duplicates."""
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None

    seed_instruments(db)
    first_count = db.add.call_count

    db.query.return_value.filter.return_value.first.return_value = MagicMock()
    seed_instruments(db)

    assert db.add.call_count == first_count


def test_instruments_list_has_correct_slugs():
    slugs = [i["slug"] for i in INSTRUMENTS]
    assert "cello" in slugs
    assert "piano" in slugs
    assert "guitar" in slugs
    assert "music-theory" in slugs