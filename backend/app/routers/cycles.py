from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_user_id
from app.models import schemas
from app.services import db
from app.services.pcod_risk import compute_pcod_risk
from app.services.date_validation import detect_date_inconsistencies, get_health_insights_from_dates
from app.services.symptom_manager import get_symptom_suggestions, get_symptom_insights, get_recommended_symptoms
from app.services.stress_analyzer import calculate_stress_score, get_stress_insights, get_stress_trend

router = APIRouter(prefix="/api/cycles", tags=["cycles"])


@router.get("", response_model=List[dict])
def list_cycles(user_id: str = Depends(get_user_id)):
    return db.list_cycles(user_id)


@router.post("", response_model=dict)
def create_cycle(
    body: schemas.CycleIn, user_id: str = Depends(get_user_id)
):
    db.ensure_user(user_id)
    d = body.model_dump()
    
    # Get existing cycles for validation
    existing_cycles = db.list_cycles(user_id)
    
    # Check for date inconsistencies
    warnings, suggestions = detect_date_inconsistencies(d, existing_cycles)
    health_insights = get_health_insights_from_dates(d, existing_cycles)
    
    cid = db.add_cycle(user_id, d)
    
    return {
        "id": cid, 
        **d,
        "alerts": {
            "warnings": warnings,
            "suggestions": suggestions,
            "health_insights": health_insights
        }
    }


@router.get("/symptoms/suggestions", response_model=dict)
def get_symptom_suggestions(q: str, limit: int = 10):
    """Get symptom suggestions for autocomplete."""
    from app.services.symptom_manager import get_symptom_suggestions
    suggestions = get_symptom_suggestions(q, limit)
    return {"suggestions": suggestions}


@router.get("/assessment/pcod", response_model=dict)
def pcod_assessment(user_id: str = Depends(get_user_id)):
    rows = db.list_cycles(user_id)
    lengths = schemas.cycle_lengths_from_rows(rows)
    risk = compute_pcod_risk(rows)
    return {**risk, "cycle_count": len(rows), "lengths_observed": lengths}


@router.patch("/{cycle_id}", response_model=dict)
def patch_cycle(
    cycle_id: str, body: schemas.CycleIn, user_id: str = Depends(get_user_id)
):
    ok = db.update_cycle(user_id, cycle_id, body.model_dump())
    if not ok:
        raise HTTPException(404, "Cycle not found")
    rows = db.list_cycles(user_id)
    for c in rows:
        if c.get("id") == cycle_id:
            return c
    return {"id": cycle_id, **body.model_dump()}


@router.delete("/{cycle_id}")
def remove_cycle(cycle_id: str, user_id: str = Depends(get_user_id)):
    if not db.delete_cycle(user_id, cycle_id):
        raise HTTPException(404, "Cycle not found")
    return {"ok": True}


@router.get("/symptoms/recommended")
def get_recommended_symptoms_endpoint(user_id: str = Depends(get_user_id)):
    """Get recommended symptoms based on user history."""
    cycles = db.list_cycles(user_id)
    recommended = get_recommended_symptoms("general")
    return {"recommended": recommended}
