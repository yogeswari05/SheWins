from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.services.auth_tokens import decode_access_token

_security = HTTPBearer(auto_error=False)


async def get_current_user_id(
    creds: HTTPAuthorizationCredentials | None = Depends(_security),
) -> str:
    if creds is None or (creds.scheme or "").lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Sign in to access your private data.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_access_token(creds.credentials)
        uid = payload.get("sub")
        if not uid:
            raise HTTPException(status_code=401, detail="Invalid token")
        return str(uid)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


# Backwards-compatible name for routers
get_user_id = get_current_user_id
