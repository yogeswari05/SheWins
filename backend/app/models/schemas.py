from __future__ import annotations

from datetime import date
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field


class CycleIn(BaseModel):
    start_date: str
    end_date: Optional[str] = None
    flow: str = Field("medium", description="light|medium|heavy")
    symptoms: List[str] = Field(default_factory=list)
    mood: str = ""
    sleep_hours: Optional[float] = None
    stress: Optional[int] = Field(None, ge=0, le=10)
    exercise: Optional[str] = None
    notes: str = ""


class CycleOut(CycleIn):
    id: str
    created_at: str = ""
    updated_at: str = ""


class ReminderIn(BaseModel):
    id: Optional[str] = None
    kind: str  # period_prediction | health_alert | custom
    title: str
    schedule_cron: Optional[str] = None
    next_due: Optional[str] = None
    active: bool = True


class ChatMessageIn(BaseModel):
    message: str
    language: str = "en"


class UserSettingsIn(BaseModel):
    locale: Optional[str] = None
    reminder_preferences: Optional[dict] = None
    opt_in_analytics: Optional[bool] = None


class SignupIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    display_name: str = Field("", max_length=120)


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str


def cycle_lengths_from_rows(rows: List[dict]) -> List[int]:
    if len(rows) < 2:
        return []
    s = sorted(rows, key=lambda c: c["start_date"])
    from datetime import datetime

    out: List[int] = []
    for i in range(1, len(s)):
        a = s[i - 1]["start_date"][:10]
        b = s[i]["start_date"][:10]
        d0 = date.fromisoformat(a)
        d1 = date.fromisoformat(b)
        out.append((d1 - d0).days)
    return out
