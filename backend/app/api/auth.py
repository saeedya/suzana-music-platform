from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.limiter import limiter
from app.core.supabase import supabase
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
def signup(request: Request, data: UserCreate) -> dict[str, object]:
    try:
        return sign_up(supabase, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/signin")
@limiter.limit("10/minute")
def signin(request: Request, data: SignInRequest) -> dict[str, object]:
    try:
        return sign_in(supabase, data.email, data.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) from e


@router.post("/signout")
def signout(data: SignOutRequest) -> dict[str, str]:
    try:
        sign_out(supabase, data.jwt)
        return {"message": "Signed out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e