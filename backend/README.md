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
- Supabase (Auth + Database)
- Pytest (testing)

## Structure

```
app/
├── api/          # route handlers
├── core/
│   ├── config.py      # settings
│   ├── database.py    # SQLAlchemy engine
│   ├── log.py         # loguru setup
│   ├── security.py    # JWT + bcrypt
│   ├── seed.py        # seed data
│   └── supabase.py    # Supabase client
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
| GET | `/api/v1/instruments/` | List all instruments |
| GET | `/api/v1/instruments/{slug}` | Get instrument by slug |
| POST | `/api/v1/auth/signup` | Sign up |
| POST | `/api/v1/auth/signin` | Sign in |
| POST | `/api/v1/auth/signout` | Sign out |
| GET | `/api/v1/courses/` | No | List published courses |
| GET | `/api/v1/courses/{slug}` | No | Course detail |
| GET | `/api/v1/courses/instrument/{id}` | No | Courses by instrument |
| POST | `/api/v1/courses/` | Admin | Create course |
| PATCH | `/api/v1/courses/{slug}` | Admin | Update course |
| DELETE | `/api/v1/courses/{slug}` | Admin | Soft delete course |

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

## Models & Schemas

| Model | Schema | Description |
|-------|--------|-------------|
| `Instrument` | `InstrumentCreate`, `InstrumentResponse` | Cello · Piano · Guitar · Music Theory |
| `User` | `UserCreate`, `UserResponse` | Students and admin (Suzana) |
| `Course` | `CourseCreate`, `CourseResponse`, `CourseUpdate` | Recorded courses per instrument |

## Services

| Service | Description |
|---------|-------------|
| `instrument_service` | get all, get by slug, create |
| `auth_service` | sign up, sign in, sign out, get user (Supabase) |
| `course_service` | get all, get by instrument, get by slug, create, update, soft delete |

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
docker run -p 8000:8000 --env-file .env suzana-backend
```

## Seed data

```bash
PYTHONPATH=. venv/bin/python app/core/seed.py
```

## Local development

### With Docker (recommended)

```bash
docker compose up --build
```

- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

### Without Docker

```bash
# Start Supabase
supabase start

# Start FastAPI
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```