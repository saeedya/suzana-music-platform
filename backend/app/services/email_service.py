import resend

from app.core.config import settings

resend.api_key = settings.resend_api_key


def send_booking_confirmation_student(
    student_email: str,
    student_name: str,
    instrument: str,
    starts_at: str,
    ends_at: str,
    room_url: str,
) -> None:
    resend.Emails.send({
        "from": settings.resend_from_email,
        "to": student_email,
        "subject": "Your lesson is confirmed!",
        "html": f"""
        <h2>Your lesson is confirmed!</h2>
        <p>Hi {student_name},</p>
        <p>Your <strong>{instrument}</strong> lesson has been confirmed.</p>
        <ul>
            <li><strong>Date:</strong> {starts_at}</li>
            <li><strong>Duration:</strong> until {ends_at}</li>
        </ul>
        <p>
            <a href="{room_url}" style="
                background-color: #6366f1;
                color: white;
                padding: 12px 24px;
                border-radius: 6px;
                text-decoration: none;
                display: inline-block;
            ">
                Join your lesson
            </a>
        </p>
        <p>See you soon!</p>
        <p>Suzana</p>
        """,
    })


def send_booking_confirmation_suzana(
    suzana_email: str,
    student_name: str,
    student_email: str,
    instrument: str,
    starts_at: str,
    ends_at: str,
    room_url: str,
) -> None:
    resend.Emails.send({
        "from": settings.resend_from_email,
        "to": suzana_email,
        "subject": f"New lesson booked — {student_name}",
        "html": f"""
        <h2>New lesson booked</h2>
        <p>A student has booked a lesson with you.</p>
        <ul>
            <li><strong>Student:</strong> {student_name} ({student_email})</li>
            <li><strong>Instrument:</strong> {instrument}</li>
            <li><strong>Date:</strong> {starts_at}</li>
            <li><strong>Duration:</strong> until {ends_at}</li>
        </ul>
        <p>
            <a href="{room_url}">Open lesson room</a>
        </p>
        """,
    })

def send_booking_cancelled_student(
    student_email: str,
    student_name: str,
    instrument: str,
    starts_at: str,
) -> None:
    resend.Emails.send({
        "from": settings.resend_from_email,
        "to": student_email,
        "subject": "Your lesson has been cancelled",
        "html": f"""
        <h2>Lesson cancelled</h2>
        <p>Hi {student_name},</p>
        <p>Your <strong>{instrument}</strong> lesson scheduled for 
        <strong>{starts_at}</strong> has been cancelled.</p>
        <p>If you paid for this lesson, a refund will be processed 
        within 5-10 business days.</p>
        <p>If you have any questions, please reply to this email.</p>
        <p>Suzana</p>
        """,
    })