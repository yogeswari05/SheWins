"""
PCOD/PCOS risk heuristics and weighted 0-100 score from cycle + symptom data.
Non-diagnostic: educational / early-warning use only.
"""
from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

HIGH_GAP_DAYS = 35
CYCLE_VARIANCE_HIGH = 15
MEDIUM_PROLONGED_BLEED = 7


@dataclass
class CycleEvent:
    start: date
    end: Optional[date] = None
    flow: str = "medium"  # light|medium|heavy
    symptoms: List[str] = field(default_factory=list)
    mood: str = ""
    sleep_hours: Optional[float] = None
    stress: Optional[int] = None
    exercise: Optional[str] = None


def _parse_date(s: str) -> date:
    if isinstance(s, date) and not isinstance(s, datetime):
        return s
    return date.fromisoformat(str(s)[:10])


def cycle_lengths(cycles: List[Dict[str, Any]]) -> List[int]:
    if len(cycles) < 2:
        return []
    starts = sorted(_parse_date(c["start_date"]) for c in cycles)
    return [(starts[i] - starts[i - 1]).days for i in range(1, len(starts))]


def high_risk_flags(cycles: List[Dict[str, Any]], lengths: List[int]) -> Tuple[int, List[str]]:
    points = 0
    notes: List[str] = []
    if not lengths and len(cycles) < 1:
        return 0, notes

    # Gaps > 35 days
    for L in lengths:
        if L > HIGH_GAP_DAYS:
            points += 25
            notes.append("gap_over_35_days")
            break

    # Skipping 2+ cycles (gaps that imply missed periods — very long gap vs median)
    if lengths:
        med = statistics.median(lengths)
        long_skips = sum(1 for L in lengths if L > med + 30 or L > 60)
        if long_skips >= 2:
            points += 30
            notes.append("multiple_skipped_or_missed")

    # Variance > 15 days
    if len(lengths) >= 3:
        var = statistics.pstdev(lengths)
        if var > CYCLE_VARIANCE_HIGH:
            points += 20
            notes.append("high_cycle_variance")

    return min(points, 70), list(dict.fromkeys(notes))


def medium_risk_flags(
    cycles: List[Dict[str, Any]], lengths: List[int]
) -> Tuple[int, List[str]]:
    points = 0
    notes: List[str] = []
    sym_lower = " ".join(" ".join(c.get("symptoms") or []) for c in cycles).lower()
    has_acne = "acne" in sym_lower
    has_weight = "weight" in sym_lower or "weight gain" in sym_lower
    has_hair = "hair" in sym_lower or "hairfall" in sym_lower or "hirsutism" in sym_lower
    if has_acne and has_weight and has_hair:
        points += 20
        notes.append("acne_weight_hair")

    for c in cycles:
        s = _parse_date(c["start_date"])
        e = c.get("end_date")
        if e:
            e_d = _parse_date(e)
            if (e_d - s).days + 1 > MEDIUM_PROLONGED_BLEED:
                points += 15
                notes.append("prolonged_bleeding")
                break

    for L in lengths:
        if 35 > L > 0 and L == max(lengths) and L >= 32:
            points += 10
            notes.append("consistently_long_cycle")

    return min(points, 45), list(dict.fromkeys(notes))


def low_risk_flags(cycles: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
    points = 0
    notes: List[str] = []
    blob = " ".join(
        " ".join(c.get("symptoms") or []) + " " + (c.get("mood") or "")
        for c in cycles
    ).lower()
    for kw, w in [
        ("mood", 5),
        ("mood swing", 8),
        ("fatigue", 8),
        ("spot", 6),
    ]:
        if kw in blob:
            points += w
            notes.append(f"low_signal_{kw.replace(' ', '_')}")
    return min(points, 25), list(dict.fromkeys(notes))[:5]


def compute_pcod_risk(
    cycles: List[Dict[str, Any]], symptoms_summary: Optional[Dict[str, int]] = None
) -> Dict[str, Any]:
    """
    Weighted 0-100 risk score. Updated conceptually 'after each cycle' by
    recomputing on full history.
    """
    if not cycles:
        return {
            "risk_score": 0,
            "level": "unknown",
            "factors": [],
            "recommendation": "Log your first period to begin assessment.",
        }

    lengths = cycle_lengths(cycles)
    h_pts, h_notes = high_risk_flags(cycles, lengths)
    m_pts, m_notes = medium_risk_flags(cycles, lengths)
    l_pts, l_notes = low_risk_flags(cycles)

    raw = h_pts * 0.5 + m_pts * 0.35 + l_pts * 0.15
    score = int(max(0, min(100, round(raw * 1.2))))

    if score >= 60:
        level = "high"
        rec = "Risk score is elevated. We recommend consulting a gynecologist for a clinical evaluation. This app does not provide a diagnosis."
    elif score >= 35:
        level = "medium"
        rec = "Some patterns may warrant a discussion with a healthcare provider. Track consistently and consider professional advice if symptoms persist."
    else:
        level = "low"
        rec = "Based on current logs, no strong PCOS pattern is detected. Continue tracking and see a doctor for any new or worsening symptoms."

    factors: List[Dict[str, str]] = []
    for n in h_notes:
        factors.append(
            {
                "tier": "high",
                "code": n,
                "label": n.replace("_", " ").title(),
            }
        )
    for n in m_notes:
        factors.append(
            {
                "tier": "medium",
                "code": n,
                "label": n.replace("_", " ").title(),
            }
        )
    for n in l_notes:
        factors.append(
            {
                "tier": "low",
                "code": n,
                "label": n.replace("_", " ").title(),
            }
        )

    return {
        "risk_score": score,
        "level": level,
        "factors": factors,
        "recommendation": rec,
        "irregularity_index": round(
            statistics.pstdev(lengths) if len(lengths) >= 2 else 0, 1
        ),
    }
