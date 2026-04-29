# Backend — Suzana Music Platform

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Pytest](https://img.shields.io/badge/tested--with-pytest-orange)
![Status](https://img.shields.io/badge/status-in--progress-yellow)
![CI](https://github.com/saeedya/suzana-music-platform/actions/workflows/ci.yaml/badge.svg)

REST API built with FastAPI and Python.

## Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Alembic (migrations)
- Pytest (testing)

## Structure

```
app/
├── api/          # route handlers
├── core/         # config, security, database
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas
└── services/     # business logic

tests/
├── unit/         # unit tests
└── integration/  # integration tests
```

## Setup

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

## Running tests

```bash
pytest tests/ -v
pytest tests/unit/ -v         # unit only
pytest tests/integration/ -v  # integration only
pytest --cov=app tests/       # with coverage
```

## Lint and type check

```bash
ruff check app/  # lint
mypy app/        # type check
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |

> Swagger UI available at `/docs` in development only.

## Security

- Passwords hashed with `bcrypt`
- Authentication via JWT (HS256)
- Tokens expire after 30 minutes
- `/docs` disabled in production
- Row Level Security (RLS) enabled on all tables
  - `instruments`: public read, admin-only write
  - `users`: users can only access their own row
  - `alembic_version`: fully restricted
- `anon` role revoked from all tables

## Models

| Model | Description |
|-------|-------------|
| `Instrument` | Cello · Piano · Guitar · Music Theory |
| `User` | Students and admin (Suzana) |

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Performance

- RLS policies use `(select ...)` to avoid per-row re-evaluation
- Indexes: `idx_users_id`, `idx_users_is_admin`, `idx_instruments_slug`

## Logging

- Development: colorized console output (DEBUG level)
- Production: JSON format (INFO level) — compatible with Grafana

## Docker

```bash
docker build -t backend .
docker run -p 8000:8000 --env-file .env backend
```