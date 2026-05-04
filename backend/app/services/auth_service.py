import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session as DBSession
from supabase import Client

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def sign_up(client: Client, data: UserCreate, db: DBSession | None = None) \
      -> dict[str, object]:
    response = client.auth.sign_up({
        "email": data.email,
        "password": data.password,
    })

    if db and response.user:
        existing = db.query(User).filter(User.email == data.email).first()
        if not existing:
            user = User(
                id=uuid.uuid4(),
                email=data.email,
                hashed_password=hash_password(data.password),
                full_name=data.full_name,
                is_active=True,
                is_admin=False,
                created_at=datetime.now(timezone.utc),
            )
            db.add(user)
            db.commit()

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