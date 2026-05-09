from unittest.mock import MagicMock, patch
from app.services.payment_service import (
    create_payment_intent,
    confirm_payment_intent,
    create_refund,
)


def test_create_payment_intent():
    with patch("app.services.payment_service.stripe.PaymentIntent.create") as mock:
        mock.return_value = MagicMock(id="pi_123", client_secret="secret_123")
        result = create_payment_intent(5000, "usd", {"booking_id": "abc"})
        mock.assert_called_once_with(
            amount=5000,
            currency="usd",
            metadata={"booking_id": "abc"},
        )
        assert result.id == "pi_123"


def test_create_payment_intent_no_metadata():
    with patch("app.services.payment_service.stripe.PaymentIntent.create") as mock:
        mock.return_value = MagicMock(id="pi_123")
        create_payment_intent(5000)
        mock.assert_called_once_with(amount=5000, currency="usd", metadata={})


def test_confirm_payment_intent():
    with patch("app.services.payment_service.stripe.PaymentIntent.retrieve") as mock:
        mock.return_value = MagicMock(id="pi_123", status="succeeded")
        result = confirm_payment_intent("pi_123")
        assert result.id == "pi_123"


def test_create_refund_full():
    with patch("app.services.payment_service.stripe.Refund.create") as mock:
        mock.return_value = MagicMock(id="re_123")
        result = create_refund("pi_123")
        mock.assert_called_once_with(payment_intent="pi_123")
        assert result.id == "re_123"


def test_create_refund_partial():
    with patch("app.services.payment_service.stripe.Refund.create") as mock:
        mock.return_value = MagicMock(id="re_123")
        result = create_refund("pi_123", amount_cents=2500)
        mock.assert_called_once_with(payment_intent="pi_123", amount=2500)
        assert result.id == "re_123"

def test_stripe_client_initialized():
    from app.core.stripe_client import stripe
    assert stripe.api_key is not None

def test_construct_webhook_event():
    with patch("app.services.payment_service.stripe.Webhook.construct_event") as mock:
        mock.return_value = MagicMock(type="payment_intent.succeeded")
        from app.services.payment_service import construct_webhook_event
        result = construct_webhook_event(b"payload", "sig_header")
        assert result is not None

def test_stripe_api_key_set_from_settings():
    from app.core.stripe_client import stripe
    from app.core.config import settings
    assert stripe.api_key == settings.stripe_secret_key