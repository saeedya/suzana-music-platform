# Design Document — Suzana Music Platform

> Version: 1.7.0
> Last updated: 2026-05-08
> Status: In progress

---

## 1. Overview

Suzana is a professional musician with 30+ years of experience. This platform allows her to:

- Offer private online lessons (cello, piano, guitar, music theory)
- Sell recorded courses
- Manage monthly subscriptions
- Accept payments from students worldwide

---

## 2. Tech Stack

### Backend
| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Language |
| FastAPI | 0.136 | API framework |
| SQLAlchemy | 2.0 | ORM |
| Alembic | 1.13 | DB migrations |
| Pydantic | 2.13 | Data validation |
| pydantic-settings | 2.2 | Config from .env |
| psycopg | 3.1 | PostgreSQL driver |
| bcrypt | 4.1 | Password hashing |
| PyJWT | 2.12 | JWT tokens |
| loguru | 0.7 | Logging |
| supabase | 2.4 | Auth + DB client |
| resend | 2.29 | Transactional Email |

### Frontend
| Tool | Version | Purpose |
|------|---------|---------|
| Next.js | 14.2 | Framework |
| React | 18 | UI library |
| TypeScript | 5 | Type safety |
| Tailwind CSS | 3 | Styling |
| axios | 1.x | HTTP client |
| @tanstack/react-query | 5 | Server state |
| zod | 3 | Validation |
| react-hook-form | 7 | Form handling |
| lucide-react | 0.x | Icons |
| Stripe.js | 3 | Payment UI |

### Current pages
| Page | Path | Type | Description |
|------|------|------|-------------|
| Landing | `/` | Server | Hero + features |
| Courses | `/courses` | Server | List all courses with instrument filter |
| Course detail | `/courses/[slug]` | Server | Course info + booking button |
| Sign in | `/auth/signin` | Client | Login form with show/hide password |
| Sign up | `/auth/signup` | Client | Register form with password validation |
| Dashboard | `/dashboard` | Client | My upcoming and past lessons |
| Booking | `/booking` | Client | 4-step wizard: instrument → duration → slot → payment |

### Infrastructure
| Tool | Purpose |
|------|---------|
| DigitalOcean NYC1 | Origin server |
| Docker + Compose | Containerization ✅ | 
| Caddy | Reverse proxy + auto HTTPS |
| Cloudflare | CDN · WAF · DNS · R2 |
| Supabase (self-hosted) | PostgreSQL + Auth ✅ |
| GitHub Actions | CI/CD ✅ |
| Grafana + Prometheus | Monitoring (planned) |
| Terraform | IaC (planned) ✅ |
| Railway | Staging deployment ✅ |

### Third-party
| Service | Purpose |
|---------|---------|
| Stripe | Payments |
| Daily.co | Live video lessons — room created after payment confirmed |
| Resend | Transactional email |
| Cloudflare R2 | Video storage + backups |

---

## 3. Database Schema

### instruments
```sql
id          uuid PRIMARY KEY DEFAULT gen_random_uuid()
name        text NOT NULL
slug        text UNIQUE NOT NULL
```

### users
```sql
id               uuid PRIMARY KEY
email            text UNIQUE NOT NULL
hashed_password  text NOT NULL
full_name        text NOT NULL
is_active        boolean DEFAULT true
is_admin         boolean DEFAULT false
created_at       timestamptz DEFAULT now()
```

### courses
```sql
id              uuid PRIMARY KEY DEFAULT gen_random_uuid()
instrument_id   uuid REFERENCES instruments(id)
title           text NOT NULL
slug            text UNIQUE NOT NULL
description     text
price_cents     integer NOT NULL
level           text  -- 'beginner' | 'intermediate' | 'advanced' | 'all'
lesson_count    integer
is_published    boolean DEFAULT false
is_active       boolean DEFAULT true
stripe_price_id text
created_at      timestamptz DEFAULT now()
```

### bookings
```sql
id                       uuid PRIMARY KEY DEFAULT gen_random_uuid()
student_id               uuid REFERENCES users(id)
instrument_id            uuid REFERENCES instruments(id)
starts_at                timestamptz NOT NULL
ends_at                  timestamptz NOT NULL
status                   text DEFAULT 'pending'
price_cents              integer NOT NULL
stripe_payment_intent_id text
daily_room_url           text
notes                    text
created_at               timestamptz DEFAULT now()
```

### availability
```sql
id               uuid PRIMARY KEY
day_of_week      integer  -- 0=Monday, 6=Sunday
start_time       time NOT NULL
end_time         time NOT NULL
session_duration integer NOT NULL  -- 30 or 60 minutes
is_active        boolean DEFAULT true
timezone         text DEFAULT 'America/New_York'
```

### subscriptions (planned)
```sql
id                     uuid PRIMARY KEY
student_id             uuid REFERENCES users(id)
stripe_subscription_id text UNIQUE NOT NULL
plan                   text  -- 'basic' | 'standard' | 'unlimited'
lessons_per_month      integer
status                 text  -- 'active' | 'cancelled' | 'past_due'
current_period_end     timestamptz
```

---

## 4. API Design

### Versioning
All endpoints prefixed with `/api/v1/`.

### Current endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/health` | No | Health check |
| GET | `/api/v1/instruments/` | No | List instruments |
| GET | `/api/v1/instruments/{slug}` | No | Get by slug |
| POST | `/api/v1/auth/signup` | No | Sign up |
| POST | `/api/v1/auth/signin` | No | Sign in |
| POST | `/api/v1/auth/signout` | Yes | Sign out |
| GET | `/api/v1/courses/` | No | List published courses |
| GET | `/api/v1/courses/{slug}` | No | Course detail |
| GET | `/api/v1/courses/instrument/{id}` | No | Courses by instrument |
| POST | `/api/v1/courses/` | Admin | Create course |
| PATCH | `/api/v1/courses/{slug}` | Admin | Update course |
| DELETE | `/api/v1/courses/{slug}` | Admin | Soft delete course |
| POST | `/api/v1/bookings/` | Yes | Book a lesson |
| GET | `/api/v1/bookings/my` | Yes | My bookings |
| GET | `/api/v1/bookings/my/{id}` | Yes | Get own booking by id |
| GET | `/api/v1/bookings/` | Admin | All bookings |
| GET | `/api/v1/bookings/{id}` | Admin | Get booking |
| PATCH | `/api/v1/bookings/{id}/cancel` | Yes | Cancel booking |
| POST | `/api/v1/payments/create-intent` | Yes | Create payment intent |
| POST | `/api/v1/payments/webhook` | No | Stripe webhook |
| GET | `/api/v1/availability/` | No | List availability |
| POST | `/api/v1/availability/` | Admin | Create availability |
| GET | `/api/v1/availability/slots` | Yes | Available slots by date |


### Planned endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/subscriptions/` | Yes | Create subscription |

---

## 5. Payment Flows

### One-time course purchase
```
1. POST /api/v1/payments/create-intent
2. FastAPI creates Stripe PaymentIntent
3. Student pays via Stripe Payment Element
4. Stripe fires payment_intent.succeeded webhook
5. FastAPI unlocks course access
6. Resend sends confirmation email
```

### Private lesson booking
```
1. POST /api/v1/bookings/
2. FastAPI checks availability
3. FastAPI creates Stripe PaymentIntent
4. Student pays
5. Stripe webhook → booking confirmed
6. Daily.co room created
7. Resend sends confirmation + room link
```

### Subscription
```
1. POST /api/v1/subscriptions/
2. Stripe Subscription created
3. customer.subscription.created webhook → DB record
4. Monthly invoice.paid → decrement lessons
```

### Refund policy
- Cancellation > 24h before lesson → full refund
- Cancellation < 24h → no refund

---

## 6. Security Decisions

### Why Supabase Auth?
- Handles signup, signin, JWT issuance
- Magic link support out of the box
- Session management handled
- Saves weeks of development time

### Why RLS?
- Database-level access control
- Independent of application code
- Even if app has a bug, data is protected
- Students can only see their own rows

### Key decisions
- `secret_key` and `database_url` required at startup — app refuses to start without them
- `/docs` disabled in production — Swagger UI only in development
- Stripe webhook signature verified with `stripe.construct_event()`
- `anon` role revoked from all tables (Supabase-specific)
- Migrations conditional on role existence — works on both Supabase and plain PostgreSQL
- Rate limiting on auth endpoints via `slowapi` — signup: 5/min, signin: 10/min per IP

### Password policy
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character (!@#$%^&*)
- Validation on frontend before submission

---

## 7. Infrastructure Decisions

### Why DigitalOcean over AWS?
- Simpler pricing — no surprise bills
- Better value for money at this scale
- Terraform provider is clean and well-documented
- NYC1 is closest to Suzana's location (Atlanta)

### Why Caddy over Nginx?
- Automatic HTTPS via Let's Encrypt — no certbot, no cron jobs
- HTTP → HTTPS redirect out of the box
- Config is dramatically simpler

### Why Cloudflare?
- Free CDN — static assets served from 300+ edge locations
- Free WAF — blocks common attack patterns
- R2 for video storage — S3-compatible, no egress fees

### Why self-hosted Supabase?
- Saves ~$25/mo vs Supabase Cloud
- Full control over data
- RLS and migrations work identically

---

## 8. Testing Strategy

### Unit tests (169 tests · 95% coverage)
- Mock all external dependencies (DB, Supabase, Stripe)
- Fast — run in under 5 seconds
- Run on every push

### Integration tests (14 tests)
- Real PostgreSQL connection
- Transaction rollback after each test — no data pollution
- Run on every push (PostgreSQL service in GitHub Actions)

### Planned
- E2E tests with Playwright (frontend)
- Stripe webhook integration tests

---

*This document is updated as the project evolves.*