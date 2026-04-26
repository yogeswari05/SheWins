from __future__ import annotations

import bcrypt

def hash_password(plain: str) -> str:
    if not plain:
        raise ValueError("empty_password")
    # bcrypt will embed the salt & cost in the resulting hash string.
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(plain.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False
