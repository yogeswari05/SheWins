from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter, Depends

from app.dependencies import get_user_id
from app.models import schemas
from app.services import db
from app.services.pcod_risk import compute_pcod_risk

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def _month_add(y: int, m: int, delta: int) -> tuple:
    m += delta
    while m < 1:
        m += 12
        y -= 1
    while m > 12:
        m -= 12
        y += 1
    return y, m


@router.get("/dashboard")
def analytics_dashboard(user_id: str = Depends(get_user_id)):
    rows = db.list_cycles(user_id)
    rows_sorted = sorted(rows, key=lambda c: c.get("start_date", ""))
    lengths = schemas.cycle_lengths_from_rows(rows_sorted)
    _ = lengths
    risk = compute_pcod_risk(rows_sorted)

    sym_counter: Counter[str] = Counter()
    for c in rows_sorted:
        for s in c.get("symptoms") or []:
            sym_counter[s] += 1

    trend: List[Dict[str, Any]] = []
    sdates = [c.get("start_date", "") for c in rows_sorted]
    for i in range(1, len(sdates)):
        a = sdates[i - 1][:10]
        b = sdates[i][:10]
        l_days = (date.fromisoformat(b) - date.fromisoformat(a)).days
        trend.append(
            {
                "index": i,
                "length_days": l_days,
                "period_start": sdates[i][:10],
            }
        )

    today = date.today()
    y, m = _month_add(today.year, today.month, -5)
    window_start = date(y, m, 1)

    on_period: set[date] = set()
    for c in rows_sorted:
        s = c.get("start_date", "")
        e = c.get("end_date")
        if not s:
            continue
        ds = date.fromisoformat(s[:10])
        if e:
            de = date.fromisoformat(e[:10])
        else:
            de = ds + timedelta(days=4)
        x = ds
        while x <= de:
            on_period.add(x)
            x += timedelta(days=1)

    # ~6 month window through end of current month
    y2, m2 = today.year, today.month
    m2 += 1
    if m2 > 12:
        m2, y2 = 1, y2 + 1
    last = date(y2, m2, 1) - timedelta(days=1)
    if last < today:
        last = today
    heat_days: List[dict] = []
    d = window_start
    while d <= last:
        heat_days.append(
            {
                "date": d.isoformat(),
                "in_period": d in on_period,
                "intensity": 1 if d in on_period else 0,
            }
        )
        d += timedelta(days=1)

    # Calculate mood patterns
    mood_counter: Counter[str] = Counter()
    mood_sleep_stress: Dict[str, List[float]] = {}
    
    for c in rows_sorted:
        mood = c.get("mood")
        if mood:
            mood_counter[mood] += 1
            if mood not in mood_sleep_stress:
                mood_sleep_stress[mood] = []
            mood_sleep_stress[mood].append(c.get("sleep_hours", 0) or 0)
            mood_sleep_stress[mood].append(c.get("stress", 0) or 0)

    mood_patterns = []
    for mood, count in mood_counter.most_common():
        avg_sleep = sum(mood_sleep_stress[mood][::2]) / len(mood_sleep_stress[mood][::2]) if mood_sleep_stress[mood][::2] else 0
        avg_stress = sum(mood_sleep_stress[mood][1::2]) / len(mood_sleep_stress[mood][1::2]) if mood_sleep_stress[mood][1::2] else 0
        mood_patterns.append({
            "mood": mood,
            "count": count,
            "avg_sleep": round(avg_sleep, 1),
            "avg_stress": round(avg_stress, 1)
        })

    # Calculate wellness metrics
    sleep_hours = [c.get("sleep_hours", 0) or 0 for c in rows_sorted if c.get("sleep_hours")]
    stress_levels = [c.get("stress", 0) or 0 for c in rows_sorted if c.get("stress")]
    exercise_types = [c.get("exercise", "none") for c in rows_sorted if c.get("exercise")]
    
    avg_sleep = sum(sleep_hours) / len(sleep_hours) if sleep_hours else 0
    avg_stress = sum(stress_levels) / len(stress_levels) if stress_levels else 0
    
    exercise_counter = Counter(exercise_types)
    exercise_frequency = [{"type": k, "count": v} for k, v in exercise_counter.most_common()]
    
    wellness_metrics = {
        "avg_sleep": round(avg_sleep, 1),
        "avg_stress": round(avg_stress, 1),
        "exercise_frequency": exercise_frequency
    }

    # Generate pre-period patterns
    pre_period_patterns = []
    if len(rows_sorted) >= 3:
        for i in range(1, min(4, len(rows_sorted))):
            current_cycle = rows_sorted[i]
            prev_cycle = rows_sorted[i-1] if i > 0 else None
            
            # Look at symptoms 3-5 days before period
            if prev_cycle and prev_cycle.get("end_date"):
                pre_period_start = date.fromisoformat(prev_cycle["end_date"][:10]) - timedelta(days=5)
                pre_period_end = date.fromisoformat(prev_cycle["end_date"][:10]) - timedelta(days=2)
                
                # Find entries in pre-period window
                pre_period_symptoms = set()
                pre_period_moods = set()
                
                # Check current cycle's symptoms that might be pre-period
                if current_cycle.get("symptoms"):
                    pre_period_symptoms.update(current_cycle["symptoms"][:3])  # Top 3 symptoms
                
                if current_cycle.get("mood"):
                    pre_period_moods.add(current_cycle["mood"])
                
                if pre_period_symptoms or pre_period_moods:
                    pre_period_patterns.append({
                        "days_before": 3,
                        "common_symptoms": list(pre_period_symptoms)[:2],
                        "common_moods": list(pre_period_moods)[:2]
                    })

    # Generate personal insights
    personal_insights = []
    
    # Sleep-stress insight
    if avg_sleep < 6 and avg_stress > 6:
        personal_insights.append({
            "type": "sleep-stress",
            "message": f"CRITICAL: You're averaging {avg_sleep:.1f}h sleep with {avg_stress:.1f}/10 stress. Fix: Go to bed 1 hour earlier + no screens 30min before bed.",
            "confidence": 0.9
        })
    elif avg_sleep >= 8 and avg_stress <= 4:
        personal_insights.append({
            "type": "sleep-stress",
            "message": f"EXCELLENT: {avg_sleep:.1f}h sleep with {avg_stress:.1f}/10 stress. Maintain this routine - it's working perfectly.",
            "confidence": 0.9
        })
    
    # Exercise-mood insight
    if exercise_counter.get("moderate", 0) > 0 or exercise_counter.get("heavy", 0) > 0:
        positive_moods = mood_counter.get("happy", 0) + mood_counter.get("calm", 0) + mood_counter.get("energetic", 0)
        total_moods = sum(mood_counter.values())
        if positive_moods > total_moods * 0.6:
            exercise_type = "moderate" if exercise_counter.get("moderate", 0) > exercise_counter.get("heavy", 0) else "heavy"
            personal_insights.append({
                "type": "exercise-mood",
                "message": f"Your {exercise_type} exercise is directly improving your mood. Continue: {exercise_counter[exercise_type]} sessions/week + add 1 more session for better results.",
                "confidence": 0.7
            })
    else:
        personal_insights.append({
            "type": "exercise-mood",
            "message": "NO EXERCISE RECORDED. Start with 10-minute walks daily + track mood changes. Exercise is essential for mood regulation.",
            "confidence": 0.8
        })

    return {
        "irregularity_index": risk.get("irregularity_index", 0),
        "pcod": risk,
        "symptom_frequency": [
            {"symptom": k, "count": v} for k, v in sym_counter.most_common(20)
        ],
        "cycle_length_trend": trend,
        "calendar_heatmap_6m": {
            "start": window_start.isoformat(),
            "days": heat_days,
        },
        "mood_patterns": mood_patterns,
        "wellness_metrics": wellness_metrics,
        "pre_period_patterns": pre_period_patterns,
        "personal_insights": personal_insights
    }
