"""
Mood prediction and analysis service for EliteHer.
Analyzes mood patterns, predicts mood changes, and provides emotional wellness insights.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple
import statistics
import numpy as np
from datetime import datetime, timedelta


def analyze_mood_patterns(cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze mood patterns across menstrual cycles.
    
    Returns:
        - Most common moods
        - Mood cycle patterns
        - Pre-period mood changes
        - Mood-symptom correlations
    """
    
    if not cycles:
        return {"patterns": [], "insights": [], "correlations": {}}
    
    mood_data = []
    for cycle in cycles:
        mood = cycle.get("mood", "").lower()
        if mood:
            cycle_date = datetime.fromisoformat(cycle.get("start_date", "")[:10])
            mood_data.append({
                "mood": mood,
                "date": cycle_date,
                "symptoms": cycle.get("symptoms", []),
                "stress": cycle.get("stress"),
                "sleep_hours": cycle.get("sleep_hours"),
                "exercise": cycle.get("exercise")
            })
    
    if not mood_data:
        return {"patterns": [], "insights": [], "correlations": {}}
    
    # Mood frequency analysis
    mood_counts = {}
    for entry in mood_data:
        mood = entry["mood"]
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    most_common_moods = sorted(mood_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Mood categories
    positive_moods = ["happy", "calm", "energetic", "loved"]
    negative_moods = ["sad", "anxious", "irritable", "unwell", "tired"]
    neutral_moods = ["confused"]
    
    positive_count = sum(mood_counts.get(mood, 0) for mood in positive_moods)
    negative_count = sum(mood_counts.get(mood, 0) for mood in negative_moods)
    neutral_count = sum(mood_counts.get(mood, 0) for mood in neutral_moods)
    
    total_moods = positive_count + negative_count + neutral_count
    
    # Calculate mood ratios
    mood_ratio = {
        "positive": positive_count / total_moods if total_moods > 0 else 0,
        "negative": negative_count / total_moods if total_moods > 0 else 0,
        "neutral": neutral_count / total_moods if total_moods > 0 else 0
    }
    
    # Analyze pre-period mood patterns
    pre_period_moods = analyze_pre_period_moods(mood_data)
    
    # Mood-symptom correlations
    correlations = analyze_mood_symptom_correlations(mood_data)
    
    # Generate insights
    insights = generate_mood_insights(mood_counts, mood_ratio, pre_period_moods, correlations)
    
    return {
        "most_common_moods": most_common_moods,
        "mood_ratio": mood_ratio,
        "pre_period_patterns": pre_period_moods,
        "correlations": correlations,
        "insights": insights,
        "total_entries": len(mood_data)
    }


def analyze_pre_period_moods(mood_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze mood changes in the days leading up to menstruation."""
    if len(mood_data) < 3:
        return {"pattern": "insufficient_data", "insights": []}
    
    # Sort by date
    mood_data.sort(key=lambda x: x["date"])
    
    pre_period_moods = []
    
    # Look for mood patterns 3-5 days before period starts
    for i in range(1, len(mood_data)):
        current_entry = mood_data[i]
        prev_entry = mood_data[i-1]
        
        # Calculate days difference
        days_diff = (current_entry["date"] - prev_entry["date"]).days
        
        # If this looks like a period start (cycle length 21-35 days)
        if 21 <= days_diff <= 35:
            # Check mood in the 3 days before this period
            pre_period_window = []
            for j in range(max(0, i-3), i):
                pre_period_window.append(mood_data[j]["mood"])
            
            if pre_period_window:
                pre_period_moods.extend(pre_period_window)
    
    if not pre_period_moods:
        return {"pattern": "no_clear_pattern", "insights": []}
    
    # Analyze pre-period mood patterns
    pre_period_counts = {}
    for mood in pre_period_moods:
        pre_period_counts[mood] = pre_period_counts.get(mood, 0) + 1
    
    # Identify dominant pre-period mood
    dominant_pre_period = max(pre_period_counts.items(), key=lambda x: x[1])
    
    # Check if negative moods increase pre-period
    negative_moods = ["sad", "anxious", "irritable", "unwell", "tired"]
    pre_period_negative_ratio = sum(pre_period_counts.get(mood, 0) for mood in negative_moods) / len(pre_period_moods)
    
    pattern = "normal"
    insights = []
    
    if pre_period_negative_ratio > 0.6:
        pattern = "premenstrual_mood_decline"
        insights.append("You tend to experience more negative moods before your period")
        insights.append("Consider self-care strategies in the week before your period")
    elif dominant_pre_period[0] in ["calm", "happy"]:
        pattern = "stable_pre_period"
        insights.append("Your mood remains relatively stable before your period")
    else:
        pattern = "variable_pre_period"
        insights.append("Your pre-period mood patterns vary - continue tracking for clarity")
    
    return {
        "pattern": pattern,
        "dominant_mood": dominant_pre_period,
        "negative_ratio": round(pre_period_negative_ratio, 2),
        "insights": insights,
        "data_points": len(pre_period_moods)
    }


def analyze_mood_symptom_correlations(mood_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze correlations between mood and physical symptoms."""
    correlations = {}
    
    # Group by mood
    mood_groups = {}
    for entry in mood_data:
        mood = entry["mood"]
        if mood not in mood_groups:
            mood_groups[mood] = []
        mood_groups[mood].append(entry)
    
    # Analyze symptom patterns for each mood
    for mood, entries in mood_groups.items():
        symptom_counts = {}
        stress_values = []
        sleep_values = []
        
        for entry in entries:
            # Count symptoms
            symptoms = entry.get("symptoms", [])
            for symptom in symptoms:
                symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
            
            # Collect stress and sleep data
            if entry.get("stress") is not None:
                stress_values.append(entry["stress"])
            if entry.get("sleep_hours") is not None:
                sleep_values.append(entry["sleep_hours"])
        
        # Calculate averages
        avg_stress = statistics.mean(stress_values) if stress_values else None
        avg_sleep = statistics.mean(sleep_values) if sleep_values else None
        
        # Find most common symptoms for this mood
        most_common_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        correlations[mood] = {
            "most_common_symptoms": most_common_symptoms,
            "average_stress": round(avg_stress, 1) if avg_stress is not None else None,
            "average_sleep": round(avg_sleep, 1) if avg_sleep is not None else None,
            "sample_size": len(entries)
        }
    
    return correlations


def generate_mood_insights(mood_counts: Dict[str, int], mood_ratio: Dict[str, float], 
                          pre_period: Dict[str, Any], correlations: Dict[str, Any]) -> List[str]:
    """Generate insights based on mood analysis."""
    insights = []
    
    # Overall mood balance
    if mood_ratio["positive"] > 0.6:
        insights.append("You generally maintain a positive mood - great emotional health!")
    elif mood_ratio["negative"] > 0.5:
        insights.append("You experience negative moods frequently - consider emotional support strategies")
    else:
        insights.append("Your mood balance is mixed - tracking helps identify patterns")
    
    # Most common mood insights
    if mood_counts:
        most_common = max(mood_counts.items(), key=lambda x: x[1])
        insights.append(f"Your most common mood is '{most_common[0]}' ({most_common[1]} times)")
    
    # Pre-period insights
    if pre_period.get("pattern") == "premenstrual_mood_decline":
        insights.append("Plan for extra self-care before your period to manage mood changes")
    
    # Stress-mood correlation insights
    high_stress_moods = []
    for mood, data in correlations.items():
        if data.get("average_stress", 0) > 6:
            high_stress_moods.append(mood)
    
    if high_stress_moods:
        insights.append(f"High stress correlates with: {', '.join(high_stress_moods)}")
    
    # Sleep-mood correlation insights
    poor_sleep_moods = []
    for mood, data in correlations.items():
        if data.get("average_sleep", 8) < 6:
            poor_sleep_moods.append(mood)
    
    if poor_sleep_moods:
        insights.append(f"Poor sleep correlates with: {', '.join(poor_sleep_moods)}")
    
    return insights[:5]  # Return top 5 insights


def predict_mood_trends(cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Predict mood trends for the upcoming cycle."""
    if len(cycles) < 3:
        return {"prediction": "insufficient_data", "confidence": 0}
    
    # Get recent mood data
    recent_cycles = sorted(cycles, key=lambda x: x.get("start_date", ""))[-6:]
    mood_sequence = []
    
    for cycle in recent_cycles:
        mood = cycle.get("mood", "").lower()
        if mood:
            mood_sequence.append(mood)
    
    if len(mood_sequence) < 3:
        return {"prediction": "insufficient_data", "confidence": 0}
    
    # Convert moods to numerical values for trend analysis
    mood_values = {
        "happy": 5, "calm": 4, "energetic": 4, "loved": 5,
        "confused": 3, "tired": 2,
        "anxious": 1, "sad": 1, "irritable": 1, "unwell": 1
    }
    
    numerical_moods = [mood_values.get(mood, 3) for mood in mood_sequence]
    
    # Calculate trend
    if len(numerical_moods) >= 3:
        x = list(range(len(numerical_moods)))
        trend_slope = np.polyfit(x, numerical_moods, 1)[0]
        
        # Predict next mood value
        next_predicted = numerical_moods[-1] + trend_slope
        
        # Convert back to mood category
        if next_predicted >= 4:
            predicted_mood = "positive"
            mood_examples = ["happy", "calm", "energetic"]
        elif next_predicted <= 2:
            predicted_mood = "negative"
            mood_examples = ["sad", "anxious", "irritable"]
        else:
            predicted_mood = "neutral"
            mood_examples = ["confused", "tired"]
        
        # Calculate confidence based on consistency
        if len(numerical_moods) > 1 and statistics.mean(numerical_moods) > 0:
            consistency = 1 - (statistics.stdev(numerical_moods) / statistics.mean(numerical_moods))
        else:
            consistency = 0
        confidence = max(0, min(1, consistency))
        
        return {
            "prediction": predicted_mood,
            "examples": mood_examples,
            "confidence": round(confidence, 2),
            "trend_slope": round(trend_slope, 2),
            "recent_moods": mood_sequence[-3:],
            "recommendation": get_mood_prediction_recommendation(predicted_mood, confidence)
        }
    
    return {"prediction": "unclear", "confidence": 0}


def get_mood_prediction_recommendation(prediction: str, confidence: float) -> str:
    """Get recommendation based on mood prediction."""
    if confidence < 0.5:
        return "Low confidence prediction - continue tracking for better accuracy"
    
    if prediction == "positive":
        return "Positive mood predicted! Maintain your current self-care routine"
    elif prediction == "negative":
        return "Challenging mood predicted - prepare extra self-care and support strategies"
    else:
        return "Neutral mood predicted - good time for maintaining emotional balance practices"


def get_mood_recommendations(current_mood: str, patterns: Dict[str, Any]) -> List[str]:
    """Get personalized mood recommendations."""
    recommendations = []
    
    # Based on current mood
    if current_mood in ["sad", "anxious", "irritable", "unwell"]:
        recommendations.extend([
            "Practice deep breathing exercises for 5 minutes",
            "Consider gentle physical activity like walking",
            "Reach out to a friend or family member",
            "Engage in a comforting activity (reading, music, bath)"
        ])
    elif current_mood in ["tired", "confused"]:
        recommendations.extend([
            "Ensure adequate rest and sleep",
            "Reduce caffeine and screen time",
            "Practice gentle stretching or yoga",
            "Write down thoughts to gain clarity"
        ])
    else:  # positive moods
        recommendations.extend([
            "Maintain your current healthy habits",
            "Share your positive energy with others",
            "Document what contributes to your good mood",
            "Plan enjoyable activities to maintain positivity"
        ])
    
    # Based on patterns
    if patterns.get("pre_period_patterns", {}).get("pattern") == "premenstrual_mood_decline":
        recommendations.append("Prepare mood support strategies for the week before your period")
    
    return recommendations[:4]  # Return top 4 recommendations
