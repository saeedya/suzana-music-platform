# Suzana Music Platform

Online music teaching platform for Suzana — a professional musician with 30+ years of experience.

## What Suzana teaches

- Cello
- Piano
- Guitar
- Music Theory

## Students

Anyone, anywhere in the world.

## Production deployment

```bash
# Pull latest image and restart
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d

# Run migrations
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

> Caddy handles HTTPS automatically via Let's Encrypt.
> Set `DOMAIN` environment variable before deploying.