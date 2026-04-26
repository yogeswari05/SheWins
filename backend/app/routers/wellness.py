"""
Wellness router for comprehensive wellness analysis and ML predictions.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import get_user_id
from app.services import db
from app.services.wellness_predictor import calculate_wellness_score, predict_wellness_trend, get_wellness_insights
from app.services.stress_analyzer import calculate_stress_score, get_stress_trend
from app.services.mood_predictor import analyze_mood_patterns, predict_mood_trends, get_mood_recommendations
from app.services.sleep_predictor import analyze_sleep_patterns, predict_sleep_trends, get_sleep_recommendations
from app.services.symptom_manager import get_symptom_insights, analyze_symptom_patterns

router = APIRouter(prefix="/api/wellness", tags=["wellness"])


@router.get("/score")
def get_wellness_score(user_id: str = Depends(get_user_id)):
    """Get comprehensive wellness score and analysis."""
    cycles = db.list_cycles(user_id)
    return calculate_wellness_score(cycles)


@router.get("/trend")
def get_wellness_trend(user_id: str = Depends(get_user_id)):
    """Predict wellness trends based on current patterns."""
    cycles = db.list_cycles(user_id)
    return predict_wellness_trend(cycles)


@router.get("/insights")
def get_wellness_insights_endpoint(user_id: str = Depends(get_user_id)):
    """Get comprehensive wellness insights."""
    cycles = db.list_cycles(user_id)
    return {"insights": get_wellness_insights(cycles)}


@router.get("/stress-analysis")
def get_stress_analysis(user_id: str = Depends(get_user_id)):
    """Get comprehensive stress analysis."""
    cycles = db.list_cycles(user_id)
    stress_scores = []
    
    for cycle in cycles:
        stress_analysis = calculate_stress_score(cycle)
        stress_scores.append({
            "cycle_id": cycle.get("id"),
            "date": cycle.get("start_date"),
            "stress_analysis": stress_analysis
        })
    
    trend = get_stress_trend(cycles)
    
    return {
        "stress_scores": stress_scores,
        "trend": trend,
        "current_stress": stress_scores[-1]["stress_analysis"] if stress_scores else None
    }


@router.get("/mood-analysis")
def get_mood_analysis(user_id: str = Depends(get_user_id)):
    """Get comprehensive mood analysis and predictions."""
    cycles = db.list_cycles(user_id)
    
    mood_patterns = analyze_mood_patterns(cycles)
    mood_trends = predict_mood_trends(cycles)
    
    # Get recommendations for current mood
    current_mood = cycles[-1].get("mood", "") if cycles else ""
    mood_recs = get_mood_recommendations(current_mood, mood_patterns) if current_mood else []
    
    return {
        "patterns": mood_patterns,
        "trends": mood_trends,
        "recommendations": mood_recs,
        "current_mood": current_mood
    }


@router.get("/sleep-analysis")
def get_sleep_analysis(user_id: str = Depends(get_user_id)):
    """Get comprehensive sleep analysis and predictions."""
    cycles = db.list_cycles(user_id)
    
    sleep_patterns = analyze_sleep_patterns(cycles)
    sleep_trends = predict_sleep_trends(cycles)
    
    # Get recommendations for current sleep
    current_sleep = cycles[-1].get("sleep_hours") if cycles else None
    sleep_recs = get_sleep_recommendations(current_sleep, sleep_patterns) if current_sleep else []
    
    return {
        "patterns": sleep_patterns,
        "trends": sleep_trends,
        "recommendations": sleep_recs,
        "current_sleep": current_sleep
    }


@router.get("/symptom-analysis")
def get_symptom_analysis(user_id: str = Depends(get_user_id)):
    """Get comprehensive symptom analysis."""
    cycles = db.list_cycles(user_id)
    
    # Get insights for current symptoms
    current_symptoms = cycles[-1].get("symptoms", []) if cycles else []
    symptom_insights = get_symptom_insights(current_symptoms)
    
    # Analyze patterns across all cycles
    symptom_patterns = analyze_symptom_patterns(cycles)
    
    return {
        "current_insights": symptom_insights,
        "patterns": symptom_patterns,
        "current_symptoms": current_symptoms
    }


@router.get("/comprehensive")
def get_comprehensive_wellness(user_id: str = Depends(get_user_id)):
    """Get all wellness data in a single comprehensive response."""
    cycles = db.list_cycles(user_id)
    
    # Get all analyses
    wellness_score = calculate_wellness_score(cycles)
    wellness_trend = predict_wellness_trend(cycles)
    wellness_insights = get_wellness_insights(cycles)
    
    mood_patterns = analyze_mood_patterns(cycles)
    mood_trends = predict_mood_trends(cycles)
    
    sleep_patterns = analyze_sleep_patterns(cycles)
    sleep_trends = predict_sleep_trends(cycles)
    
    current_cycle = cycles[-1] if cycles else {}
    
    return {
        "overall_wellness": {
            "score": wellness_score,
            "trend": wellness_trend,
            "insights": wellness_insights
        },
        "mood": {
            "patterns": mood_patterns,
            "trends": mood_trends,
            "current": current_cycle.get("mood", "")
        },
        "sleep": {
            "patterns": sleep_patterns,
            "trends": sleep_trends,
            "current": current_cycle.get("sleep_hours")
        },
        "stress": {
            "current": calculate_stress_score(current_cycle) if current_cycle else None,
            "trend": get_stress_trend(cycles)
        },
        "symptoms": {
            "current": current_cycle.get("symptoms", []),
            "insights": get_symptom_insights(current_cycle.get("symptoms", [])) if current_cycle else None
        },
        "data_summary": {
            "total_cycles": len(cycles),
            "date_range": {
                "earliest": min(c.get("start_date", "") for c in cycles) if cycles else None,
                "latest": max(c.get("start_date", "") for c in cycles) if cycles else None
            }
        }
    }
