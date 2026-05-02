# Email Flow — Suzana Music Platform

> Powered by Resend

---

## Emails sent

| Trigger | Recipient | Subject |
|---------|-----------|---------|
| Booking confirmed (after payment) | Student | Your lesson is confirmed! |
| Booking confirmed (after payment) | Suzana | New lesson booked — {student_name} |

---

## Booking confirmed flow

```
1. Student pays via Stripe
2. Stripe fires payment_intent.succeeded webhook
3. FastAPI confirms booking
4. FastAPI creates Daily.co room
5. FastAPI sends email to student — room link + lesson details
6. FastAPI sends email to Suzana — student info + lesson details
```

---

## Email sender

| Environment | From address |
|-------------|--------------|
| Development | `onboarding@resend.dev` |
| Production | `lessons@suzana.com` (custom domain — planned) |

---

## Planned emails

- **Booking reminder** — 24h before lesson → student + Suzana
- **Booking cancelled** — cancellation confirmed → student
- **Refund processed** — refund confirmed → student

---

## Notes

- Suzana's email is configured via `SUZANA_EMAIL` env var (planned)
- Currently hardcoded as placeholder in `payments.py`
- HTML templates are inline — React Email templates planned for production