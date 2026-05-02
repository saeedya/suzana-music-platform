from unittest.mock import patch
from app.services.email_service import (
    send_booking_confirmation_student,
    send_booking_confirmation_suzana,
)


def test_send_booking_confirmation_student():
    with patch("app.services.email_service.resend.Emails.send") as mock_send:
        send_booking_confirmation_student(
            student_email="student@example.com",
            student_name="John Doe",
            instrument="Cello",
            starts_at="Monday, May 01 2026 at 10:00 UTC",
            ends_at="11:00 UTC",
            room_url="https://suzana-music.daily.co/booking-abc",
        )
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0][0]
        assert call_args["to"] == "student@example.com"
        assert "confirmed" in call_args["subject"].lower()
        assert "John Doe" in call_args["html"]
        assert "Cello" in call_args["html"]


def test_send_booking_confirmation_suzana():
    with patch("app.services.email_service.resend.Emails.send") as mock_send:
        send_booking_confirmation_suzana(
            suzana_email="suzana@example.com",
            student_name="John Doe",
            student_email="student@example.com",
            instrument="Piano",
            starts_at="Monday, May 01 2026 at 10:00 UTC",
            ends_at="11:00 UTC",
            room_url="https://suzana-music.daily.co/booking-abc",
        )
        mock_send.assert_called_once()
        call_args = mock_send.call_args[0][0]
        assert call_args["to"] == "suzana@example.com"
        assert "John Doe" in call_args["subject"]
        assert "Piano" in call_args["html"]