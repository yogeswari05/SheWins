from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_user_id
from app.models.schemas import UserSettingsIn
from app.services import db
from app.services import encryption

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/me")
def me(user_id: str = Depends(get_user_id)):
    db.ensure_user(user_id)
    return db.get_user(user_id) or {"id": user_id, "settings": {}}


@router.post("/init")
def init(
    user_id: str = Depends(get_user_id),
    locale: str = Query("en"),
    display_name: str = Query(""),
):
    db.ensure_user(user_id)
    payload: dict = {"locale": locale}
    if display_name:
        payload["display_name_enc"] = encryption.maybe_encrypt_str(display_name)
    db.merge_user_data(user_id, payload)
    u = db.get_user(user_id) or {}
    s = (u.get("settings") or {}) if isinstance(u, dict) else {}
    s["locale"] = locale
    db.update_user_settings(user_id, s)
    return {"id": user_id, "locale": locale}


@router.patch("/settings")
def patch_settings(
    body: UserSettingsIn, user_id: str = Depends(get_user_id)
):
    prev_opt = bool((db.get_user(user_id) or {}).get("opt_in_analytics") or False)
    existing = (db.get_user(user_id) or {}).get("settings") or {}
    m = {**existing}
    d = body.model_dump(exclude_none=True)
    if d:
        m.update(d)
    db.update_user_settings(user_id, m)
    if body.locale is not None:
        db.merge_user_data(user_id, {"locale": body.locale})
    if body.opt_in_analytics is not None:
        new_opt = bool(body.opt_in_analytics)
        db.merge_user_data(user_id, {"opt_in_analytics": new_opt})
        if new_opt != prev_opt:
            db.anon_record_opt_in_delta(1 if new_opt else -1)
    return {"ok": True, "settings": m}
