from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import get_user_id
from app.models import schemas
from app.services import db
from app.services import ml_predictor
from app.services import sklearn_signals
from app.services.enhanced_predictor import enhanced_predictor

router = APIRouter(prefix="/api/predict", tags=["ml"])


@router.get("/cycles")
def predict_cycles(user_id: str = Depends(get_user_id)):
    rows = db.list_cycles(user_id)
    lengths = schemas.cycle_lengths_from_rows(rows)
    pred = ml_predictor.predict_next_cycles(lengths)
    pred["sklearn_irregularity_fraction"] = sklearn_signals.isolation_irregularity_score(
        lengths
    )
    return pred


@router.get("/enhanced")
def predict_cycles_enhanced(user_id: str = Depends(get_user_id)):
    """Enhanced prediction with pattern analysis and insights."""
    rows = db.list_cycles(user_id)
    lengths = schemas.cycle_lengths_from_rows(rows)
    enhanced_pred = enhanced_predictor.predict_with_insights(lengths)
    
    # Add sklearn irregularity score
    enhanced_pred["sklearn_irregularity_fraction"] = sklearn_signals.isolation_irregularity_score(
        lengths
    )
    
    return enhanced_pred
