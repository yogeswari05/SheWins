"""
Stress analysis service that calculates stress scores from user inputs.
Uses multiple factors including sleep, symptoms, mood, exercise, and text analysis.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


# Stress-related keywords for text analysis
STRESS_KEYWORDS = {
    "high_stress": [
        "overwhelmed", "anxious", "worried", "stressed", "tense", "nervous",
        "panic", "pressure", "burden", "exhausted", "burnout", "frustrated",
        "irritable", "angry", "mad", "upset", "distressed", "uneasy"
    ],
    "medium_stress": [
        "tired", "fatigued", "busy", "rushed", "concerned", "apprehensive",
        "troubled", "disturbed", "agitated", "restless", "fidgety", "on edge"
    ],
    "low_stress": [
        "calm", "relaxed", "peaceful", "content", "comfortable", "at ease",
        "serene", "tranquil", "rested", "refreshed", "energized", "positive"
    ]
}

# Physical symptoms that indicate stress
STRESS_SYMPTOMS = {
    "high": ["headache", "migraine", "chest_pain", "rapid_heartbeat", "shortness_of_breath"],
    "medium": ["muscle_tension", "jaw_clenching", "stomach_issues", "digestive_problems", "fatigue"],
    "low": ["mild_tension", "restlessness", "difficulty_concentrating"]
}

# Mood indicators for stress
STRESS_MOODS = {
    "high": ["anxious", "irritable", "angry", "overwhelmed", "panicked"],
    "medium": ["worried", "concerned", "uneasy", "restless", "agitated"],
    "low": ["calm", "peaceful", "content", "relaxed", "happy"]
}


def analyze_text_stress(text: str) -> Dict[str, Any]:
    """Analyze text input for stress indicators."""
    if not text:
        return {"score": 0, "indicators": [], "confidence": 0}
    
    text_lower = text.lower()
    stress_indicators = []
    high_count = 0
    medium_count = 0
    low_count = 0
    
    # Count stress keywords
    for keyword in STRESS_KEYWORDS["high_stress"]:
        if keyword in text_lower:
            high_count += 1
            stress_indicators.append(f"high_stress_keyword:{keyword}")
    
    for keyword in STRESS_KEYWORDS["medium_stress"]:
        if keyword in text_lower:
            medium_count += 1
            stress_indicators.append(f"medium_stress_keyword:{keyword}")
    
    for keyword in STRESS_KEYWORDS["low_stress"]:
        if keyword in text_lower:
            low_count += 1
            stress_indicators.append(f"low_stress_keyword:{keyword}")
    
    # Calculate text-based stress score
    total_indicators = high_count + medium_count + low_count
    if total_indicators == 0:
        text_score = 0
        confidence = 0
    else:
        # Weighted score: high=3, medium=2, low=1
        weighted_score = (high_count * 3 + medium_count * 2 + low_count * 1)
        text_score = min(10, weighted_score / max(1, total_indicators) * 3)
        confidence = min(1, total_indicators / 5)  # More indicators = higher confidence
    
    return {
        "score": text_score,
        "indicators": stress_indicators,
        "confidence": confidence,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count
    }


def calculate_stress_score(cycle_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate comprehensive stress score (0-10) from multiple factors.
    
    Factors considered:
    1. Direct stress rating (if provided)
    2. Sleep hours
    3. Exercise level
    4. Mood
    5. Symptoms
    6. Text analysis (notes)
    7. Flow intensity
    """
    
    factors = []
    weighted_scores = []
    
    # 1. Direct stress rating (highest weight: 30%)
    direct_stress = cycle_data.get("stress")
    if direct_stress is not None and 0 <= direct_stress <= 10:
        weighted_scores.append({"source": "direct", "score": direct_stress, "weight": 0.3})
        factors.append(f"Direct stress rating: {direct_stress}/10")
    
    # 2. Sleep analysis (weight: 20%)
    sleep_hours = cycle_data.get("sleep_hours")
    if sleep_hours is not None:
        if sleep_hours < 5:
            sleep_stress = 8  # Very high stress
        elif sleep_hours < 6:
            sleep_stress = 6  # High stress
        elif sleep_hours < 7:
            sleep_stress = 4  # Medium stress
        elif sleep_hours <= 8:
            sleep_stress = 2  # Low stress
        elif sleep_hours <= 9:
            sleep_stress = 1  # Very low stress
        else:
            sleep_stress = 3  # Too much sleep can indicate stress
        
        weighted_scores.append({"source": "sleep", "score": sleep_stress, "weight": 0.2})
        factors.append(f"Sleep analysis: {sleep_hours} hours = stress {sleep_stress}/10")
    
    # 3. Exercise level (weight: 15%)
    exercise = cycle_data.get("exercise", "").lower()
    exercise_stress_map = {
        "none": 7,      # No exercise = higher stress
        "light": 4,     # Light exercise = moderate stress
        "moderate": 2,  # Moderate exercise = low stress
        "heavy": 5      # Heavy exercise = can increase stress
    }
    exercise_stress = exercise_stress_map.get(exercise, 5)
    weighted_scores.append({"source": "exercise", "score": exercise_stress, "weight": 0.15})
    factors.append(f"Exercise level: {exercise} = stress {exercise_stress}/10")
    
    # 4. Mood analysis (weight: 15%)
    mood = cycle_data.get("mood", "").lower()
    mood_stress = 5  # default
    
    for stress_level, moods in STRESS_MOODS.items():
        if mood in moods:
            if stress_level == "high":
                mood_stress = 8
            elif stress_level == "medium":
                mood_stress = 6
            else:
                mood_stress = 2
            break
    
    weighted_scores.append({"source": "mood", "score": mood_stress, "weight": 0.15})
    factors.append(f"Mood analysis: {mood} = stress {mood_stress}/10")
    
    # 5. Symptom analysis (weight: 10%)
    symptoms = cycle_data.get("symptoms", [])
    symptom_stress_score = 0
    stress_symptom_count = 0
    
    if isinstance(symptoms, list):
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for stress_level, symptom_list in STRESS_SYMPTOMS.items():
                if symptom_lower in symptom_list:
                    if stress_level == "high":
                        symptom_stress_score += 3
                        stress_symptom_count += 1
                    elif stress_level == "medium":
                        symptom_stress_score += 2
                        stress_symptom_count += 1
                    else:
                        symptom_stress_score += 1
                        stress_symptom_count += 1
                    break
    
    # Normalize symptom stress score
    if stress_symptom_count > 0:
        symptom_stress = min(10, symptom_stress_score / stress_symptom_count * 2)
    else:
        symptom_stress = 3  # Neutral if no stress symptoms
    
    weighted_scores.append({"source": "symptoms", "score": symptom_stress, "weight": 0.1})
    factors.append(f"Symptom analysis: {stress_symptom_count} stress symptoms = stress {symptom_stress:.1f}/10")
    
    # 6. Text analysis of notes (weight: 10%)
    notes = cycle_data.get("notes", "")
    text_analysis = analyze_text_stress(notes)
    text_stress = text_analysis["score"]
    weighted_scores.append({"source": "text", "score": text_stress, "weight": 0.1})
    if text_analysis["confidence"] > 0:
        factors.append(f"Text analysis: {len(text_analysis['indicators'])} indicators = stress {text_stress:.1f}/10")
    
    # Calculate weighted average
    if weighted_scores:
        total_weighted_score = sum(item["score"] * item["weight"] for item in weighted_scores)
        total_weight = sum(item["weight"] for item in weighted_scores)
        final_stress_score = total_weighted_score / total_weight
    else:
        final_stress_score = 5  # Default neutral
    
    # Round to 1 decimal place
    final_stress_score = round(final_stress_score, 1)
    
    # Determine stress level
    if final_stress_score >= 7:
        stress_level = "high"
        recommendation = "High stress detected. Consider relaxation techniques, deep breathing, or consulting a healthcare provider."
    elif final_stress_score >= 4:
        stress_level = "moderate"
        recommendation = "Moderate stress levels. Try gentle exercise, mindfulness, or talking with a friend."
    else:
        stress_level = "low"
        recommendation = "Stress levels appear manageable. Keep maintaining your healthy habits!"
    
    return {
        "stress_score": final_stress_score,
        "stress_level": stress_level,
        "recommendation": recommendation,
        "factors": factors,
        "weighted_components": weighted_scores,
        "text_analysis": text_analysis if text_analysis["confidence"] > 0 else None
    }


def get_stress_insights(stress_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate insights and recommendations based on stress analysis."""
    insights = []
    score = stress_data.get("stress_score", 0)
    
    # High stress insights
    if score >= 7:
        insights.append({
            "type": "warning",
            "title": "High Stress Detected",
            "message": "Your stress levels are elevated. This can affect your menstrual cycle and overall health.",
            "actionable": True,
            "suggestions": [
                "Try deep breathing exercises for 5 minutes",
                "Consider a gentle walk or yoga",
                "Talk to a friend or family member",
                "Ensure you're getting enough sleep"
            ]
        })
    
    # Sleep-specific insights
    sleep_factor = next((f for f in stress_data.get("weighted_components", []) if f["source"] == "sleep"), None)
    if sleep_factor and sleep_factor["score"] >= 6:
        insights.append({
            "type": "sleep",
            "title": "Sleep & Stress Connection",
            "message": "Poor sleep is significantly impacting your stress levels.",
            "actionable": True,
            "suggestions": [
                "Aim for 7-9 hours of sleep per night",
                "Create a relaxing bedtime routine",
                "Avoid screens 1 hour before bed",
                "Keep your bedroom cool and dark"
            ]
        })
    
    # Exercise insights
    exercise_factor = next((f for f in stress_data.get("weighted_components", []) if f["source"] == "exercise"), None)
    if exercise_factor and exercise_factor["score"] >= 6:
        insights.append({
            "type": "exercise",
            "title": "Movement for Stress Relief",
            "message": "Regular physical activity can help manage stress effectively.",
            "actionable": True,
            "suggestions": [
                "Try 20 minutes of moderate exercise daily",
                "Consider yoga or tai chi for stress reduction",
                "Even a short walk can help clear your mind",
                "Find an activity you genuinely enjoy"
            ]
        })
    
    # Text analysis insights
    text_analysis = stress_data.get("text_analysis")
    if text_analysis and text_analysis["confidence"] > 0.5:
        if text_analysis["high_count"] > 0:
            insights.append({
                "type": "emotional",
                "title": "Emotional Awareness",
                "message": "Your notes suggest you're experiencing significant emotional stress.",
                "actionable": True,
                "suggestions": [
                    "Journaling can help process emotions",
                    "Consider talking to a counselor or therapist",
                    "Practice mindfulness meditation",
                    "Be kind to yourself during difficult times"
                ]
            })
    
    return insights


def get_stress_trend(cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze stress trends across multiple cycles."""
    if len(cycles) < 2:
        return {"trend": "insufficient_data", "message": "Need at least 2 cycles for trend analysis"}
    
    stress_scores = []
    for cycle in cycles:
        stress_analysis = calculate_stress_score(cycle)
        stress_scores.append(stress_analysis["stress_score"])
    
    if len(stress_scores) < 2:
        return {"trend": "insufficient_data", "message": "Need at least 2 cycles with stress data"}
    
    # Calculate trend
    recent_avg = sum(stress_scores[-3:]) / len(stress_scores[-3:])
    earlier_avg = sum(stress_scores[:-3]) / len(stress_scores[:-3]) if len(stress_scores) > 3 else stress_scores[0]
    
    if recent_avg > earlier_avg + 1:
        trend = "increasing"
        message = "Your stress levels have been increasing recently."
    elif recent_avg < earlier_avg - 1:
        trend = "decreasing"
        message = "Your stress levels have been improving recently!"
    else:
        trend = "stable"
        message = "Your stress levels have been relatively stable."
    
    return {
        "trend": trend,
        "message": message,
        "current_average": round(recent_avg, 1),
        "previous_average": round(earlier_avg, 1),
        "scores": stress_scores,
        "insight": get_stress_trend_insight(trend, recent_avg)
    }


def get_stress_trend_insight(trend: str, current_avg: float) -> str:
    """Get specific insight based on stress trend."""
    if trend == "increasing":
        return "Consider identifying stress triggers and developing coping strategies."
    elif trend == "decreasing":
        return "Great job! Continue with your current stress management techniques."
    else:
        return "Maintain your current routines, but consider small improvements if stress is high."
