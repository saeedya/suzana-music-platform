"""
Script to create an admin user.
Usage: PYTHONPATH=. venv/bin/python app/core/create_admin.py
"""

import getpass
import uuid
from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


def create_admin(
    email: str,
    password: str,
    full_name: str,
) -> None:
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User {email} already exists.")
            return

        admin = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            is_admin=True,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    print("Create admin user")
    email = input("Email: ")
    full_name = input("Full name: ")
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm password: ")

    if password != confirm:
        print("Passwords do not match.")
        exit(1)

    if len(password) < 8:
        print("Password must be at least 8 characters.")
        exit(1)

    create_admin(email=email, password=password, full_name=full_name)