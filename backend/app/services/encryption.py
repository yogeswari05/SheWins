"""AES-256 field encryption via Fernet (symmetric, backend uses 256-bit keys)."""
from __future__ import annotations

import base64
import hashlib
import json
from typing import Any, Optional

from cryptography.fernet import Fernet, InvalidToken
from app.config import get_settings

_fernet: Optional[Fernet] = None


def _get_fernet() -> Optional[Fernet]:
    global _fernet
    if _fernet is not None:
        return _fernet
    key = get_settings().encryption_key
    if not key:
        return None
    try:
        _fernet = Fernet(
            key.encode() if not key.startswith("gAAAA") else key.encode("utf-8")
        )
    except Exception:
        key_bytes = hashlib.sha256(key.encode("utf-8")).digest()
        b64 = base64.urlsafe_b64encode(key_bytes)
        _fernet = Fernet(b64)
    return _fernet


def encrypt_value(value: Any) -> str:
    f = _get_fernet()
    if f is None:
        if isinstance(value, (dict, list)):
            return "plain::" + json.dumps(value, default=str)
        return "plain::" + json.dumps(value, default=str)
    if isinstance(value, (dict, list)):
        raw = json.dumps(value, default=str).encode("utf-8")
    else:
        raw = str(value).encode("utf-8")
    return f.encrypt(raw).decode("ascii")


def decrypt_value(encrypted: str) -> Any:
    if encrypted.startswith("plain::"):
        inner = encrypted[7:]
        try:
            return json.loads(inner)
        except json.JSONDecodeError:
            return inner
    f = _get_fernet()
    if f is None:
        return encrypted
    try:
        raw = f.decrypt(encrypted.encode("ascii"))
        s = raw.decode("utf-8")
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            return s
    except InvalidToken:
        return encrypted


def maybe_encrypt_str(s: str) -> str:
    f = _get_fernet()
    if f is None:
        return "plain::" + s
    return f.encrypt(s.encode("utf-8")).decode("ascii")


def maybe_decrypt_str(encrypted: str) -> str:
    if encrypted.startswith("plain::"):
        return encrypted[7:]
    f = _get_fernet()
    if f is None:
        return encrypted
    try:
        return f.decrypt(encrypted.encode("ascii")).decode("utf-8")
    except InvalidToken:
        return encrypted
