# Stripe Payment Flow

## Overview

Card details never touch our server — Stripe.js handles them directly in the browser.

## Payment flow diagram

```mermaid
sequenceDiagram
    participant B as Student browser
    participant F as FastAPI
    participant S as Stripe

    B->>F: POST /api/v1/bookings/
    F->>S: create PaymentIntent
    S-->>F: client_secret
    F-->>B: client_secret

    Note over B,S: Card details go directly to Stripe — never to FastAPI

    B->>S: card details (Stripe.js)
    S-->>B: payment confirmed

    Note over F,S: Stripe fires a webhook

    S->>F: POST /webhook (payment_intent.succeeded)
    F->>F: verify signature (stripe.construct_event)
    F->>F: update booking → confirmed
    F->>F: create Daily.co room
    F->>F: send email via Resend
```

## Key concepts

**PaymentIntent** — an object in Stripe representing a payment. FastAPI creates it and returns a `client_secret`.

**Stripe.js** — a JavaScript library that collects card details directly in the browser. Card numbers never reach our server.

**Webhook** — when payment succeeds, Stripe sends an HTTP POST to FastAPI. We verify the signature before processing.

**API keys:**
| Key | Used in | Public? |
|-----|---------|---------|
| `publishable_key` | Frontend (Stripe.js) | Yes |
| `secret_key` | FastAPI only | No — never expose |
| `webhook_secret` | FastAPI webhook handler | No |

## Refund policy

- Cancellation > 24h before lesson → full refund via `stripe.refunds.create()`
- Cancellation < 24h → no refund