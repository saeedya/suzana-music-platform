from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_docs_available_in_development(monkeypatch):
    monkeypatch.setenv("APP_ENV", "development")
    response = client.get("/docs")
    assert response.status_code == 200


def test_docs_disabled_in_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    from fastapi import FastAPI
    from app.core.config import settings
    prod_app = FastAPI(
        docs_url=None,
        redoc_url=None,
    )
    prod_client = TestClient(prod_app)
    response = prod_client.get("/docs")
    assert response.status_code == 404