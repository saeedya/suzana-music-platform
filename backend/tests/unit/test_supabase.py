from unittest.mock import patch, MagicMock
from app.core.supabase import supabase
from app.core.config import settings

def test_supabase_client_is_initialized():
    """Supabase client should be initialized."""
    assert supabase is not None


def test_supabase_client_uses_correct_url():
    """Supabase client should use URL from settings."""
    with patch("app.core.supabase.create_client") as mock_create:
        mock_create.return_value = MagicMock()
        from app.core import supabase as supabase_module
        supabase_module.create_client(
            settings.supabase_url,
            settings.supabase_service_role_key,
        )
        call_args = mock_create.call_args[0]
        assert call_args[0] == settings.supabase_url
        assert call_args[1] == settings.supabase_service_role_key