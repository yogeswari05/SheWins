from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends

from app.dependencies import get_user_id
from app.models import schemas
from app.services import db
from app.services.pcod_risk import compute_pcod_risk
from app.services import ml_predictor

router = APIRouter(prefix="/api/insights", tags=["insights"])


@router.get("/smart")
def smart_insights(user_id: str = Depends(get_user_id)):
    rows = sorted(db.list_cycles(user_id), key=lambda c: c.get("start_date", ""))
    lengths = schemas.cycle_lengths_from_rows(rows)
    risk = compute_pcod_risk(rows)
    pred = ml_predictor.predict_next_cycles(lengths)
    alerts: list[dict] = []
    if risk.get("risk_score", 0) > 60:
        alerts.append(
            {
                "severity": "high",
                "code": "gynecologist_recommended",
                "text": "Risk score > 60% — see a gynecologist for proper evaluation (non-diagnostic).",
            }
        )
    for L in lengths:
        if L > 35:
            alerts.append(
                {
                    "severity": "medium",
                    "code": "long_gap",
                    "text": f"One recorded gap was {L} days (>35) — log consistently and discuss if recurring.",
                }
            )
            break
    next_period_hint = None
    if rows and pred.get("next_cycles"):
        last = date.fromisoformat(rows[-1]["start_date"][:10])
        try:
            n0 = float(pred["next_cycles"][0]["predicted_length_days"])
        except Exception:
            n0 = 28.0
        nxt = last + timedelta(days=n0)
        next_period_hint = nxt.isoformat()
    return {
        "pcod": risk,
        "prediction": pred,
        "alerts": alerts,
        "next_period_estimate": next_period_hint,
    }
