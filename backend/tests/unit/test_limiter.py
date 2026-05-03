from app.core.limiter import limiter


def test_limiter_initialized():
    assert limiter is not None


def test_limiter_key_func():
    from slowapi.util import get_remote_address
    assert limiter._key_func == get_remote_address