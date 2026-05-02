import httpx

from app.core.config import settings


def create_room(booking_id: str, starts_at: float, ends_at: float) -> str:
    """Create a Daily.co room and return the room URL."""
    headers = {
        "Authorization": f"Bearer {settings.daily_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": f"booking-{booking_id}",
        "properties": {
            "nbf": int(starts_at) - 300,   # 5 min before
            "exp": int(ends_at) + 300,     # 5 min after
            "max_participants": 2,
            "enable_chat": True,
            "enable_screenshare": True,
        },
    }
    response = httpx.post(
        f"{settings.daily_api_url}/rooms",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()
    data: dict[str, str] = response.json()
    return data["url"]


def delete_room(booking_id: str) -> None:
    """Delete a Daily.co room after the lesson."""
    headers = {
        "Authorization": f"Bearer {settings.daily_api_key}",
    }
    response = httpx.delete(
        f"{settings.daily_api_url}/rooms/booking-{booking_id}",
        headers=headers,
    )
    response.raise_for_status()