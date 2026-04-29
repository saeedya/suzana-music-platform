from supabase import Client

from app.schemas.user import UserCreate


def sign_up(client: Client, data: UserCreate) -> dict[str, object]:
    response = client.auth.sign_up({
        "email": data.email,
        "password": data.password,
    })
    return {"user": response.user, "session": response.session}


def sign_in(client: Client, email: str, password: str) -> dict[str, object]:
    response = client.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })
    return {"user": response.user, "session": response.session}


def sign_out(client: Client, jwt: str) -> None:
    client.auth.sign_out()


def get_user(client: Client, jwt: str) -> dict[str, object] | None:
    response = client.auth.get_user(jwt)
    if not response or not response.user:
        return None
    return {"id": response.user.id, "email": response.user.email}