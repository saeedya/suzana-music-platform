# Backend — Suzana Music Platform

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Pytest](https://img.shields.io/badge/tested--with-pytest-orange)
![Status](https://img.shields.io/badge/status-in--progress-yellow)

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

## Models

| Model | Description |
|-------|-------------|
| `Instrument` | Cello · Piano · Guitar · Music Theory |