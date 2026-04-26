"""
Symptom management service for EliteHer.
Provides symptom suggestions, insights, and recommendations.
"""
from __future__ import annotations

from typing import List, Dict, Any


# Comprehensive symptom list for menstrual health tracking
COMPREHENSIVE_SYMPTOMS = [
    # Physical symptoms
    "cramps", "headache", "migraine", "bloating", "breast_tenderness",
    "back_pain", "fatigue", "nausea", "acne", "hair_loss",
    "weight_gain", "food_cravings", "appetite_changes", "digestive_issues",
    "constipation", "diarrhea", "dizziness", "hot_flashes", "cold_sweats",
    
    # Emotional symptoms
    "mood_swings", "irritability", "anxiety", "depression", "sadness",
    "anger", "crying_spells", "feeling_overwhelmed", "low_energy", "motivation_loss",
    
    # Cognitive symptoms
    "brain_fog", "difficulty_concentrating", "memory_issues", "confusion",
    
    # Sleep symptoms
    "insomnia", "excessive_sleep", "restless_sleep", "night_sweats",
    
    # Reproductive symptoms
    "irregular_periods", "heavy_bleeding", "spotting", "missed_periods",
    "painful_intercourse", "vaginal_dryness", "pelvic_pain",
    
    # PCOD-specific symptoms
    "excess_hair_growth", "thinning_hair", "irregular_cycles", "cysts",
    "insulin_resistance", "weight_gain_abdominal", "dark_patches",
    
    # General wellness
    "stress", "exercise_changes", "libido_changes", "skin_issues"
]


def get_symptom_suggestions(query: str, limit: int = 10) -> List[str]:
    """Get symptom suggestions based on user query."""
    query_lower = query.lower().strip()
    if not query_lower or len(query_lower) < 2:
        return []
    
    suggestions = []
    
    # Exact matches
    for symptom in COMPREHENSIVE_SYMPTOMS:
        if symptom == query_lower:
            suggestions.append(symptom)
    
    # Starts with
    for symptom in COMPREHENSIVE_SYMPTOMS:
        if symptom.startswith(query_lower) and symptom not in suggestions:
            suggestions.append(symptom)
            if len(suggestions) >= limit:
                break
    
    # Contains
    for symptom in COMPREHENSIVE_SYMPTOMS:
        if query_lower in symptom and symptom not in suggestions:
            suggestions.append(symptom)
            if len(suggestions) >= limit:
                break
    
    return suggestions[:limit]


def get_symptom_insights(symptoms: List[str]) -> Dict[str, Any]:
    """Get insights based on reported symptoms."""
    insights = {
        "severity": "mild",
        "categories": [],
        "recommendations": [],
        "potential_concerns": [],
        "wellness_tips": []
    }
    
    if not symptoms:
        return insights
    
    # Categorize symptoms
    physical = [s for s in symptoms if s in ["cramps", "headache", "migraine", "bloating", "back_pain", "fatigue"]]
    emotional = [s for s in symptoms if s in ["mood_swings", "irritability", "anxiety", "depression", "sadness"]]
    pcod_related = [s for s in symptoms if s in ["irregular_cycles", "excess_hair_growth", "weight_gain_abdominal", "cysts"]]
    
    if physical:
        insights["categories"].append("physical")
    if emotional:
        insights["categories"].append("emotional")
    if pcod_related:
        insights["categories"].append("pcod_related")
    
    # Determine severity
    if len(symptoms) > 8 or len(pcod_related) > 0:
        insights["severity"] = "moderate"
    if len(symptoms) > 12 or len(pcod_related) > 2:
        insights["severity"] = "severe"
    
    # Recommendations
    if "cramps" in symptoms:
        insights["recommendations"].append("Apply heat pack to lower abdomen")
        insights["recommendations"].append("Consider gentle stretching")
    
    if "headache" in symptoms or "migraine" in symptoms:
        insights["recommendations"].append("Stay hydrated")
        insights["recommendations"].append("Rest in dark, quiet room")
    
    if emotional:
        insights["recommendations"].append("Practice deep breathing exercises")
        insights["recommendations"].append("Consider meditation or yoga")
    
    if pcod_related:
        insights["potential_concerns"].append("Consider consulting healthcare provider about PCOD")
        insights["recommendations"].append("Maintain regular exercise routine")
        insights["recommendations"].append("Focus on balanced nutrition")
    
    # Wellness tips
    insights["wellness_tips"] = [
        "Track symptoms consistently to identify patterns",
        "Maintain regular sleep schedule",
        "Stay hydrated throughout the day",
        "Consider stress management techniques"
    ]
    
    return insights


def get_recommended_symptoms(user_profile: str = "general") -> List[str]:
    """Get recommended symptoms to track based on user profile."""
    if user_profile == "pcod_concern":
        return [
            "irregular_cycles", "excess_hair_growth", "weight_gain_abdominal",
            "acne", "mood_swings", "cramps", "fatigue", "stress"
        ]
    elif user_profile == "wellness":
        return [
            "cramps", "mood_swings", "fatigue", "stress", "sleep_quality",
            "exercise_changes", "appetite_changes"
        ]
    else:
        return [
            "cramps", "headache", "bloating", "mood_swings", "fatigue",
            "stress", "sleep_quality", "appetite_changes"
        ]


def analyze_symptom_patterns(symptoms_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze patterns in symptom history."""
    if not symptoms_history:
        return {"patterns": [], "trends": [], "insights": []}
    
    patterns = []
    trends = []
    insights = []
    
    # Most common symptoms
    symptom_counts = {}
    for entry in symptoms_history:
        symptoms = entry.get("symptoms", [])
        for symptom in symptoms:
            symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
    
    if symptom_counts:
        most_common = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        patterns.append(f"Most frequent symptoms: {', '.join([s for s, _ in most_common])}")
    
    # Severity trends
    recent_severity = []
    for entry in symptoms_history[-6:]:  # Last 6 cycles
        symptom_count = len(entry.get("symptoms", []))
        if symptom_count > 10:
            recent_severity.append("high")
        elif symptom_count > 5:
            recent_severity.append("moderate")
        else:
            recent_severity.append("low")
    
    if recent_severity:
        if recent_severity[-1] == "high":
            trends.append("Recent increase in symptom severity")
        elif all(s == recent_severity[0] for s in recent_severity):
            trends.append(f"Consistent {recent_severity[0]} symptom levels")
    
    # Insights
    if len(symptom_counts) > 8:
        insights.append("Wide variety of symptoms - consider comprehensive health review")
    
    if "stress" in symptom_counts and symptom_counts["stress"] > len(symptoms_history) * 0.7:
        insights.append("Stress is consistently reported - focus on stress management")
    
    return {
        "patterns": patterns,
        "trends": trends,
        "insights": insights,
        "symptom_frequency": symptom_counts
    }
