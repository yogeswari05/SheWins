from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models.schemas import LoginIn, SignupIn, TokenOut
from app.services import auth_password, auth_tokens, db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=TokenOut)
def signup(body: SignupIn):
    try:
        ph = auth_password.hash_password(body.password)
        uid = db.create_registered_user(
            body.email,
            ph,
            display_name=body.display_name.strip(),
            locale="en",
        )
    except ValueError as e:
        if str(e) == "email_taken":
            raise HTTPException(409, "An account with this email already exists.")
        raise HTTPException(400, str(e)) from e
    em = str(body.email).lower()
    token = auth_tokens.create_access_token(uid, em)
    return TokenOut(access_token=token, user_id=uid, email=em)


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn):
    row = db.find_user_by_email(str(body.email))
    if not row:
        raise HTTPException(401, "Invalid email or password.")
    uid, phash = row
    if not auth_password.verify_password(body.password, phash):
        raise HTTPException(401, "Invalid email or password.")
    em = str(body.email).lower()
    token = auth_tokens.create_access_token(uid, em)
    return TokenOut(access_token=token, user_id=uid, email=em)
