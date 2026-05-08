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
├── app/
│   ├── page.tsx                    # Landing page
│   ├── layout.tsx                  # Root layout
│   ├── globals.css                 # Global styles
│   ├── auth/
│   │   ├── signin/                 # Sign in page
│   │   └── signup/                 # Sign up page
│   ├── courses/
│   │   ├── page.tsx                # Courses list
│   │   └── [slug]/                 # Course detail
│   ├── dashboard/                  # My bookings
│   └── booking/
│       ├── page.tsx                # 4-step booking wizard
│       └── confirmation/           # Booking confirmation
├── components/
│   ├── booking/
│   │   ├── InstrumentStep.tsx
│   │   ├── DurationStep.tsx
│   │   ├── SlotStep.tsx
│   │   └── PaymentStep.tsx
│   ├── course/
│   │   └── BookingButton.tsx
│   └── layout/
│       └── Navbar.tsx
├── context/
│   └── AuthContext.tsx
├── lib/
│   ├── api.ts                      # axios client
│   ├── auth.ts                     # Auth functions
│   ├── availability.ts             # Availability API
│   ├── bookings.ts                 # Bookings API
│   ├── courses.ts                  # Courses API
│   └── instruments.ts              # Instruments API
└── types/
└── index.ts                    # TypeScript interfaces
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
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...

In production:

NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...

## Pages

| Page | Path | Type | Description |
|------|------|------|-------------|
| Landing | `/` | Server | Hero + features |
| Courses | `/courses` | Server | List all courses with instrument filter |
| Course detail | `/courses/[slug]` | Server | Course info + booking button |
| Sign in | `/auth/signin` | Client | Login form |
| Sign up | `/auth/signup` | Client | Register form |
| Dashboard | `/dashboard` | Client | My upcoming and past lessons |
| Booking | `/booking` | Client | 4-step wizard: instrument → duration → slot → payment · instrument step skipped if courseId in URL |
| Confirmation | `/booking/confirmation` | Client | Booking confirmed + join lesson link |

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
  -e NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_... \
  music-platform-frontend
```

### Notes

- Backend must run with `--host 0.0.0.0` for Docker to reach it
- On Linux, use machine IP instead of `localhost` or `host.docker.internal`
- Image size: ~156MB (Alpine-based)