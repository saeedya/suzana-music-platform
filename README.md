# Suzana Music Platform

Online music teaching platform for Suzana — a professional musician with 30+ years of experience teaching cello, piano, guitar, and music theory to students worldwide.

![CI](https://github.com/saeedya/suzana-music-platform/actions/workflows/ci.yaml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in--progress-yellow)

## What Suzana teaches

- Cello
- Piano
- Guitar
- Music Theory

## Students

Anyone, anywhere in the world.

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 · TypeScript · Tailwind CSS |
| Backend | FastAPI · Python 3.12 · PostgreSQL |
| Auth | Supabase Auth |
| Payments | Stripe |
| Video | Daily.co |
| Infrastructure | DigitalOcean · Docker · Caddy · Cloudflare |
| CI/CD | GitHub Actions |

## Project structure

- `backend/` — FastAPI
- `frontend/` — Next.js
- `infra/terraform` - Terraform IaC
- `docker-compose.yml`
- `docker-compose.prod.yml`
- `Caddyfile`
- `ARCHITECTURE.md`
- `DESIGN.md`
- `SECURITY.md`

## Documentation

- [Architecture](./ARCHITECTURE.md) — system design and infrastructure
- [Design document](./DESIGN.md) — technical decisions
- [Security](./SECURITY.md) — security policy and known issues

## Live demo

> These URLs are for development and testing only.
> Production will be deployed to DigitalOcean.

- Frontend: https://terrific-fulfillment-production-814a.up.railway.app
- Backend API: https://suzana-music-platform-production.up.railway.app
- Health check: https://suzana-music-platform-production.up.railway.app/api/v1/health

## Local development

### With Docker Compose (recommended)

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

### Without Docker

```bash
# 1. Start Supabase
supabase start

# 2. Start backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. Start frontend
cd frontend
npm run dev
```

## Create admin user

```bash
cd backend
source venv/bin/activate
PYTHONPATH=. venv/bin/python app/core/create_admin.py
```

## Production deployment

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

> Caddy handles HTTPS automatically via Let's Encrypt.
> Set `DOMAIN` environment variable before deploying.