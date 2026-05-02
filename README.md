# Suzana Music Platform

Online music teaching platform for Suzana — a professional musician with 30+ years of experience teaching cello, piano, guitar, and music theory to students worldwide.

![CI](https://github.com/saeedya/suzana-music-platform/actions/workflows/ci.yml/badge.svg)
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

```text
suzana-music-platform/
├── backend/          # FastAPI
├── frontend/         # Next.js (coming soon)
├── docker-compose.yml
├── docker-compose.prod.yml
├── Caddyfile
├── ARCHITECTURE.md
└── DESIGN.md
```

## Documentation

- [Architecture](./ARCHITECTURE.md) — system design and infrastructure
- [Design document](./DESIGN.md) — technical decisions

## Local development

### With Docker

```bash
docker compose up --build
```

- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

### Without Docker

```bash
supabase start
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

## Production deployment

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

> Caddy handles HTTPS automatically via Let's Encrypt.
> Set `DOMAIN` environment variable before deploying.