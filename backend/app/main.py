from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="Suzana Music Platform",
    version="0.1.0",
    docs_url="/docs" if settings.app_env != "production" else None,
    redoc_url="/redoc" if settings.app_env != "production" else None,
)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    return {"status": "ok"}