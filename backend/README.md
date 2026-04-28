# Backend — Suzana Music Platform

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