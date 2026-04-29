from fastapi import FastAPI

from app.api.instruments import router as instruments_router
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="Suzana Music Platform",
    version="0.1.0",
    docs_url="/docs" if settings.app_env != "production" else None,
    redoc_url="/redoc" if settings.app_env != "production" else None,
)

app.include_router(instruments_router)
@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}