from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.limiter import limiter
from app.core.supabase import supabase
from app.models import User
from app.schemas.user import UserCreate
from app.services.auth_service import sign_in, sign_out, sign_up

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class SignInRequest(BaseModel):
    email: str
    password: str


class SignOutRequest(BaseModel):
    jwt: str


@router.post("/signup")
@limiter.limit("5/minute")
def signup(
    request: Request,
    data: UserCreate,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        result = sign_up(supabase, data, db)
        session = result["session"]
        access_token = session.access_token if hasattr(session, "access_token") else ""
        user = db.query(User).filter(User.email == data.email).first()
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id) if user else "",
                "email": data.email,
                "full_name": user.full_name if user else "",
                "is_admin": user.is_admin if user else False,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/signin")
@limiter.limit("10/minute")
def signin(
    request: Request,
    data: SignInRequest,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        result = sign_in(supabase, data.email, data.password)
        session = result["session"]
        access_token = session.access_token if hasattr(session, "access_token") else ""
        user = db.query(User).filter(User.email == data.email).first()
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id) if user else "",
                "email": data.email,
                "full_name": user.full_name if user else "",
                "is_admin": user.is_admin if user else False,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


@router.post("/signout")
def signout(data: SignOutRequest) -> dict[str, str]:
    try:
        sign_out(supabase, data.jwt)
        return {"message": "Signed out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e