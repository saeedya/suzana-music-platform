from unittest.mock import MagicMock, patch
from app.services.daily_service import create_room, delete_room


def test_create_room_success():
    with patch("app.services.daily_service.httpx.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"url": "https://suzana-music.daily.co/booking-abc123"}
        mock_post.return_value = mock_response

        result = create_room("abc123", 1234567890.0)

        assert result == "https://suzana-music.daily.co/booking-abc123"
        mock_post.assert_called_once()
        mock_response.raise_for_status.assert_called_once()


def test_create_room_calls_correct_endpoint():
    with patch("app.services.daily_service.httpx.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"url": "https://suzana-music.daily.co/booking-abc"}
        mock_post.return_value = mock_response

        create_room("abc", 1234567890.0)

        call_kwargs = mock_post.call_args
        assert "rooms" in call_kwargs[0][0]
        assert call_kwargs[1]["json"]["name"] == "booking-abc"
        assert call_kwargs[1]["json"]["properties"]["max_participants"] == 2


def test_delete_room_success():
    with patch("app.services.daily_service.httpx.delete") as mock_delete:
        mock_response = MagicMock()
        mock_delete.return_value = mock_response

        delete_room("abc123")

        mock_delete.assert_called_once()
        mock_response.raise_for_status.assert_called_once()