"""
PCOD/PCOS risk detection using a trained Random Forest model.
Non-diagnostic: educational / early-warning use only.
"""
from __future__ import annotations

import statistics
import pickle
from pathlib import Path
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

_model = None

def _model_path() -> Path:
    base = Path(__file__).resolve().parent.parent.parent
    return base / "models" / "pcod_rf_model.pkl"

def _load_model():
    global _model
    if _model is not None:
        return _model
    p = _model_path()
    if not p.exists():
        return None
    with open(p, "rb") as f:
        _model = pickle.load(f)
    return _model

def _parse_date(s: str) -> date:
    if isinstance(s, date) and not isinstance(s, datetime):
        return s
    return date.fromisoformat(str(s)[:10])

def cycle_lengths(cycles: List[Dict[str, Any]]) -> List[int]:
    if len(cycles) < 2:
        return []
    starts = sorted(_parse_date(c["start_date"]) for c in cycles)
    return [(starts[i] - starts[i - 1]).days for i in range(1, len(starts))]

def extract_features(cycles: List[Dict[str, Any]]) -> List[float]:
    lengths = cycle_lengths(cycles)
    cycle_variance = float(np.var(lengths)) if len(lengths) >= 2 else 5.0
    max_gap = float(np.max(lengths)) if len(lengths) >= 1 else 30.0

    acne_severity = 0
    weight_gain_score = 0
    hairfall_score = 0
    fatigue_score = 0

    # Aggregate symptoms
    sym_lower = " ".join(" ".join(c.get("symptoms") or []) for c in cycles).lower()
    
    if "acne" in sym_lower: acne_severity = 5
    if "weight" in sym_lower or "weight gain" in sym_lower: weight_gain_score = 5
    if "hair" in sym_lower or "hairfall" in sym_lower or "hirsutism" in sym_lower: hairfall_score = 5
    if "fatigue" in sym_lower: fatigue_score = 5

    return [cycle_variance, max_gap, acne_severity, weight_gain_score, hairfall_score, fatigue_score]

def compute_pcod_risk(
    cycles: List[Dict[str, Any]], symptoms_summary: Optional[Dict[str, int]] = None
) -> Dict[str, Any]:
    """
    ML-based risk score.
    """
    if not cycles:
        return {
            "risk_score": 0,
            "level": "unknown",
            "factors": [],
            "recommendation": "Log your first period to begin assessment.",
        }

    lengths = cycle_lengths(cycles)
    model = _load_model()
    
    if model is None:
        return {
            "risk_score": 0,
            "level": "unknown",
            "factors": [],
            "recommendation": "PCOD model not available.",
        }

    features = extract_features(cycles)
    prob = model.predict_proba([features])[0][1] # Probability of class 1 (PCOD)
    score = int(prob * 100)

    if score >= 60:
        level = "high"
        rec = "Risk score is elevated. We recommend consulting a gynecologist for a clinical evaluation. This app does not provide a diagnosis."
    elif score >= 35:
        level = "medium"
        rec = "Some patterns may warrant a discussion with a healthcare provider. Track consistently and consider professional advice if symptoms persist."
    else:
        level = "low"
        rec = "Based on current logs, no strong PCOS pattern is detected. Continue tracking and see a doctor for any new or worsening symptoms."

    # Identify contributing factors naively based on thresholds
    factors: List[Dict[str, str]] = []
    if features[0] > 15: factors.append({"tier": "high", "code": "high_cycle_variance", "label": "High Cycle Variance"})
    if features[1] > 35: factors.append({"tier": "high", "code": "long_cycle_gaps", "label": "Long Cycle Gaps"})
    if features[2] > 0: factors.append({"tier": "medium", "code": "acne", "label": "Acne"})
    if features[3] > 0: factors.append({"tier": "medium", "code": "weight_gain", "label": "Weight Gain"})
    if features[4] > 0: factors.append({"tier": "medium", "code": "hairfall", "label": "Hairfall/Hirsutism"})

    return {
        "risk_score": score,
        "level": level,
        "factors": factors,
        "recommendation": rec,
        "irregularity_index": round(features[0] ** 0.5 if len(lengths) >= 2 else 0, 1),
    }
