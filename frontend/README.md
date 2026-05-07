# Frontend — Music Lesson Platform

![Next.js](https://img.shields.io/badge/Next.js-14.2-black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3-38bdf8)

## Stack

- Next.js 14.2 (App Router)
- React 18
- TypeScript 5
- Tailwind CSS 3
- axios — HTTP client
- @tanstack/react-query — server state
- zod — validation
- react-hook-form — form handling
- lucide-react — icons
- Stripe.js — payment UI

## Structure

```
src/
├── app/                  # Pages (Next.js App Router)
│   ├── page.tsx          # Landing page
│   ├── layout.tsx        # Root layout
│   ├── globals.css       # Global styles
│   ├── auth/
│   │   ├── signin/       # Sign in page
│   │   └── signup/       # Sign up page
│   └── courses/          # Courses list page
├── components/
│   └── layout/
│       └── Navbar.tsx    # Navigation bar
├── context/
│   └── AuthContext.tsx   # Auth state management
├── lib/
│   ├── api.ts            # axios client
│   └── auth.ts           # Auth functions
└── types/
└── index.ts          # TypeScript interfaces
```

## Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## Environment variables

NEXT_PUBLIC_API_URL=http://localhost:8000

In production:

NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app

## Pages

| Page | Path | Type | Description |
|------|------|------|-------------|
| Landing | `/` | Server | Hero + features |
| Courses | `/courses` | Server | List all courses |
| Sign in | `/auth/signin` | Client | Login form |
| Sign up | `/auth/signup` | Client | Register form |

## Planned pages

| Page | Path | Description |
|------|------|-------------|
| Course detail | `/courses/[slug]` | Course info + booking |
| Dashboard | `/dashboard` | My bookings |
| Booking | `/booking` | Book a lesson |
| Booking | `/booking` | Client | 4-step booking wizard |

## Running in development

```bash
# Start backend first
cd ../backend
source venv/bin/activate
uvicorn app.main:app --reload

# Then start frontend
cd ../frontend
npm run dev
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

## Docker

### Build

```bash
docker build -t music-platform-frontend .
```

### Run

```bash
# Development (with local backend)
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://$(hostname -I | awk '{print $1}'):8000 \
  music-platform-frontend
```

### Notes

- Backend must run with `--host 0.0.0.0` for Docker to reach it
- On Linux, use machine IP instead of `localhost` or `host.docker.internal`
- Image size: ~156MB (Alpine-based)