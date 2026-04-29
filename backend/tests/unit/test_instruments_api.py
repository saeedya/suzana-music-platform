from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)


def make_instrument_response(name: str, slug: str) -> dict:
    return {"id": str(uuid.uuid4()), "name": name, "slug": slug}


def test_list_instruments_returns_200():
    with patch("app.api.instruments.get_all_instruments") as mock:
        mock.return_value = [
            make_instrument_response("Cello", "cello"),
            make_instrument_response("Piano", "piano"),
        ]
        response = client.get("/api/v1/instruments/")
        assert response.status_code == 200
        assert len(response.json()) == 2


def test_list_instruments_empty():
    with patch("app.api.instruments.get_all_instruments") as mock:
        mock.return_value = []
        response = client.get("/api/v1/instruments/")
        assert response.status_code == 200
        assert response.json() == []


def test_get_instrument_by_slug_found():
    with patch("app.api.instruments.get_instrument_by_slug") as mock:
        mock.return_value = make_instrument_response("Cello", "cello")
        response = client.get("/api/v1/instruments/cello")
        assert response.status_code == 200
        assert response.json()["slug"] == "cello"


def test_get_instrument_by_slug_not_found():
    with patch("app.api.instruments.get_instrument_by_slug") as mock:
        mock.return_value = None
        response = client.get("/api/v1/instruments/unknown")
        assert response.status_code == 404
        assert response.json()["detail"] == "Instrument not found"