from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import get_user_id
from app.models.schemas import ReminderIn
from app.services import db
router = APIRouter(prefix="/api/reminders", tags=["reminders"])


@router.get("")
def get_reminders(user_id: str = Depends(get_user_id)):
    return db.list_reminders(user_id)


@router.put("")
def put_reminders(
    body: List[ReminderIn], user_id: str = Depends(get_user_id)
):
    db.ensure_user(user_id)
    items = [b.model_dump() for b in body]
    db.set_reminders(user_id, items)
    return {"ok": True, "count": len(items)}
