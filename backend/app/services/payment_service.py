import stripe

from app.core.config import settings


def create_payment_intent(
    amount_cents: int,
    currency: str = "usd",
    metadata: dict[str, str] | None = None,
) -> stripe.PaymentIntent:
    return stripe.PaymentIntent.create(
        amount=amount_cents,
        currency=currency,
        metadata=metadata or {},
    )


def confirm_payment_intent(payment_intent_id: str) -> stripe.PaymentIntent:
    return stripe.PaymentIntent.retrieve(payment_intent_id)


def create_refund(
    payment_intent_id: str,
    amount_cents: int | None = None,
) -> stripe.Refund:
    if amount_cents:
        return stripe.Refund.create(
            payment_intent=payment_intent_id,
            amount=amount_cents,
        )
    return stripe.Refund.create(payment_intent=payment_intent_id)


def construct_webhook_event(payload: bytes, sig_header: str) -> stripe.Event:
    event: stripe.Event = stripe.Webhook.construct_event(  # type: ignore[no-untyped-call]
        payload, sig_header, settings.stripe_webhook_secret
    )
    return event