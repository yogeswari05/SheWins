"""
Wellness prediction service that analyzes sleep, stress, exercise, and mood patterns.
Provides comprehensive wellness insights and recommendations.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple
import statistics
import numpy as np

from app.services.stress_analyzer import calculate_stress_score, get_stress_trend


def calculate_wellness_score(cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate comprehensive wellness score (0-100) based on multiple factors.
    
    Factors considered:
    1. Sleep quality and consistency
    2. Stress levels and trends
    3. Exercise patterns
    4. Mood stability
    5. Symptom patterns
    6. Cycle regularity
    """
    
    if not cycles:
        return {
            "wellness_score": 0,
            "factors": {},
            "recommendations": ["Start tracking your cycles to get wellness insights"],
            "trend": "insufficient_data"
        }
    
    factor_scores = {}
    
    # 1. Sleep Analysis (25% weight)
    sleep_data = [c.get("sleep_hours") for c in cycles if c.get("sleep_hours") is not None]
    if sleep_data:
        avg_sleep = statistics.mean(sleep_data)
        sleep_consistency = 1 - (statistics.stdev(sleep_data) / avg_sleep) if len(sleep_data) > 1 and avg_sleep > 0 else 1
        
        # Score sleep: 7-9 hours is ideal
        if 7 <= avg_sleep <= 9:
            sleep_score = 100
        elif 6 <= avg_sleep < 7 or 9 < avg_sleep <= 10:
            sleep_score = 80
        elif 5 <= avg_sleep < 6 or 10 < avg_sleep <= 11:
            sleep_score = 60
        else:
            sleep_score = 40
        
        # Adjust for consistency
        sleep_score *= sleep_consistency
        factor_scores["sleep"] = round(sleep_score, 1)
    else:
        factor_scores["sleep"] = 50  # Neutral if no data
    
    # 2. Stress Analysis (25% weight)
    stress_scores = []
    for cycle in cycles:
        stress_analysis = calculate_stress_score(cycle)
        stress_scores.append(stress_analysis["stress_score"])
    
    if stress_scores:
        avg_stress = statistics.mean(stress_scores)
        # Convert stress to wellness score (inverse relationship)
        stress_wellness = max(0, 100 - (avg_stress * 10))
        factor_scores["stress"] = round(stress_wellness, 1)
    else:
        factor_scores["stress"] = 50
    
    # 3. Exercise Analysis (20% weight)
    exercise_data = [c.get("exercise", "").lower() for c in cycles if c.get("exercise")]
    if exercise_data:
        exercise_scores = {"none": 30, "light": 60, "moderate": 90, "heavy": 75}
        exercise_values = [exercise_scores.get(ex, 50) for ex in exercise_data]
        avg_exercise = statistics.mean(exercise_values)
        factor_scores["exercise"] = round(avg_exercise, 1)
    else:
        factor_scores["exercise"] = 50
    
    # 4. Mood Analysis (15% weight)
    mood_data = [c.get("mood", "").lower() for c in cycles if c.get("mood")]
    if mood_data:
        positive_moods = ["happy", "calm", "energetic", "loved"]
        neutral_moods = ["tired", "confused"]
        negative_moods = ["sad", "anxious", "irritable", "unwell"]
        
        positive_count = sum(1 for mood in mood_data if mood in positive_moods)
        negative_count = sum(1 for mood in mood_data if mood in negative_moods)
        
        total_moods = len(mood_data)
        if total_moods > 0:
            mood_ratio = (positive_count - negative_count) / total_moods
            mood_wellness = max(0, min(100, 50 + (mood_ratio * 50)))
            factor_scores["mood"] = round(mood_wellness, 1)
        else:
            factor_scores["mood"] = 50
    else:
        factor_scores["mood"] = 50
    
    # 5. Symptom Analysis (10% weight)
    symptom_counts = [len(c.get("symptoms", [])) for c in cycles]
    if symptom_counts:
        avg_symptoms = statistics.mean(symptom_counts)
        # Fewer symptoms generally indicate better wellness
        symptom_wellness = max(0, 100 - (avg_symptoms * 5))
        factor_scores["symptoms"] = round(symptom_wellness, 1)
    else:
        factor_scores["symptoms"] = 50
    
    # 6. Cycle Regularity (5% weight)
    cycle_lengths = []
    for i, cycle in enumerate(sorted(cycles, key=lambda x: x.get("start_date", ""))):
        if i > 0:
            prev_date = cycles[i-1].get("start_date")
            curr_date = cycle.get("start_date")
            if prev_date and curr_date:
                from datetime import datetime
                prev = datetime.fromisoformat(prev_date[:10])
                curr = datetime.fromisoformat(curr_date[:10])
                cycle_lengths.append((curr - prev).days)
    
    if cycle_lengths and len(cycle_lengths) >= 2:
        mean_cycle_length = statistics.mean(cycle_lengths)
        # Only calculate regularity if mean_cycle_length is valid (not zero)
        if mean_cycle_length > 0:
            # Only calculate standard deviation if we have multiple values
            if len(cycle_lengths) > 2:
                regularity = 1 - (statistics.stdev(cycle_lengths) / mean_cycle_length)
            else:
                # With only 2 values, calculate simple regularity based on difference
                diff = abs(cycle_lengths[1] - cycle_lengths[0])
                regularity = 1 - (diff / mean_cycle_length)
            regularity_wellness = max(0, min(100, regularity * 100))
            factor_scores["regularity"] = round(regularity_wellness, 1)
        else:
            factor_scores["regularity"] = 50
    else:
        factor_scores["regularity"] = 50
    
    # Calculate overall wellness score with weights
    weights = {
        "sleep": 0.25,
        "stress": 0.25,
        "exercise": 0.20,
        "mood": 0.15,
        "symptoms": 0.10,
        "regularity": 0.05
    }
    
    overall_score = sum(factor_scores[factor] * weights[factor] for factor in weights)
    overall_score = round(overall_score, 1)
    
    # Generate recommendations
    recommendations = generate_wellness_recommendations(factor_scores, overall_score)
    
    # Determine trend
    if len(cycles) >= 6:
        recent_cycles = cycles[-3:]
        earlier_cycles = cycles[-6:-3]
        
        recent_wellness = calculate_wellness_score(recent_cycles)["wellness_score"]
        earlier_wellness = calculate_wellness_score(earlier_cycles)["wellness_score"]
        
        if recent_wellness > earlier_wellness + 5:
            trend = "improving"
        elif recent_wellness < earlier_wellness - 5:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "wellness_score": overall_score,
        "factors": factor_scores,
        "recommendations": recommendations,
        "trend": trend,
        "data_points": len(cycles)
    }


def generate_wellness_recommendations(factor_scores: Dict[str, float], overall_score: float) -> List[str]:
    """Generate personalized wellness recommendations."""
    recommendations = []
    
    # Sleep recommendations
    if factor_scores.get("sleep", 0) < 70:
        recommendations.append("Focus on improving sleep: aim for 7-9 hours with consistent bedtime")
    
    # Stress recommendations
    if factor_scores.get("stress", 0) < 70:
        recommendations.append("Try stress management techniques: deep breathing, meditation, or gentle exercise")
    
    # Exercise recommendations
    if factor_scores.get("exercise", 0) < 70:
        recommendations.append("Increase physical activity: aim for 30 minutes of moderate exercise daily")
    
    # Mood recommendations
    if factor_scores.get("mood", 0) < 70:
        recommendations.append("Prioritize emotional health: journaling, talking with friends, or professional support")
    
    # Symptom recommendations
    if factor_scores.get("symptoms", 0) < 70:
        recommendations.append("Track symptoms consistently to identify patterns and triggers")
    
    # Overall recommendations based on score
    if overall_score >= 80:
        recommendations.append("Excellent wellness! Maintain your current healthy habits")
    elif overall_score >= 60:
        recommendations.append("Good progress! Focus on consistency in your self-care routine")
    elif overall_score >= 40:
        recommendations.append("Room for improvement: start with small, manageable changes")
    else:
        recommendations.append("Consider consulting a healthcare provider for personalized guidance")
    
    return recommendations[:5]  # Return top 5 recommendations


def predict_wellness_trend(cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Predict future wellness trends based on current patterns."""
    if len(cycles) < 3:
        return {"prediction": "insufficient_data", "confidence": 0}
    
    # Calculate wellness scores for recent cycles
    wellness_scores = []
    for i in range(3, len(cycles) + 1):
        subset = cycles[max(0, i-3):i]
        score = calculate_wellness_score(subset)["wellness_score"]
        wellness_scores.append(score)
    
    if len(wellness_scores) < 2:
        return {"prediction": "insufficient_data", "confidence": 0}
    
    # Simple linear trend prediction
    x = list(range(len(wellness_scores)))
    trend_slope = np.polyfit(x, wellness_scores, 1)[0]
    
    # Predict next score
    next_score = wellness_scores[-1] + trend_slope
    
    # Determine prediction
    if trend_slope > 1:
        prediction = "improving"
        message = "Your wellness is likely to improve based on current trends"
    elif trend_slope < -1:
        prediction = "declining"
        message = "Your wellness may need attention - consider preventive measures"
    else:
        prediction = "stable"
        message = "Your wellness is likely to remain stable"
    
    # Calculate confidence based on consistency
    if len(wellness_scores) >= 3 and wellness_scores:
        mean_score = statistics.mean(wellness_scores)
        if mean_score > 0:
            consistency = 1 - (statistics.stdev(wellness_scores) / mean_score)
            confidence = max(0, min(1, consistency))
        else:
            confidence = 0.5
    else:
        confidence = 0.5
    
    return {
        "prediction": prediction,
        "next_predicted_score": round(max(0, min(100, next_score)), 1),
        "message": message,
        "confidence": round(confidence, 2),
        "trend_slope": round(trend_slope, 2),
        "historical_scores": wellness_scores
    }


def get_wellness_insights(cycles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate comprehensive wellness insights."""
    insights = []
    
    if not cycles:
        return insights
    
    wellness_analysis = calculate_wellness_score(cycles)
    factor_scores = wellness_analysis["factors"]
    
    # Sleep insights
    sleep_score = factor_scores.get("sleep", 0)
    if sleep_score < 60:
        insights.append({
            "type": "sleep",
            "priority": "high",
            "title": "Sleep Needs Attention",
            "message": "Poor sleep is impacting your overall wellness significantly.",
            "action_items": [
                "Set a consistent bedtime routine",
                "Avoid screens 1 hour before bed",
                "Keep bedroom cool and dark",
                "Consider relaxation techniques before sleep"
            ]
        })
    elif sleep_score > 85:
        insights.append({
            "type": "sleep",
            "priority": "positive",
            "title": "Excellent Sleep Habits",
            "message": "Your sleep patterns are supporting your wellness effectively.",
            "action_items": [
                "Maintain your current sleep schedule",
                "Share your sleep routine with others who might benefit"
            ]
        })
    
    # Stress insights
    stress_score = factor_scores.get("stress", 0)
    if stress_score < 60:
        insights.append({
            "type": "stress",
            "priority": "high",
            "title": "Stress Management Needed",
            "message": "High stress levels are affecting your wellness.",
            "action_items": [
                "Practice daily mindfulness or meditation",
                "Ensure regular physical activity",
                "Consider talking to a counselor or therapist",
                "Identify and reduce stress triggers where possible"
            ]
        })
    
    # Exercise insights
    exercise_score = factor_scores.get("exercise", 0)
    if exercise_score < 60:
        insights.append({
            "type": "exercise",
            "priority": "medium",
            "title": "Increase Physical Activity",
            "message": "Regular exercise would significantly improve your wellness.",
            "action_items": [
                "Start with 10-15 minute daily walks",
                "Find an activity you genuinely enjoy",
                "Consider group activities for motivation",
                "Set realistic, achievable exercise goals"
            ]
        })
    
    # Mood insights
    mood_score = factor_scores.get("mood", 0)
    if mood_score < 60:
        insights.append({
            "type": "mood",
            "priority": "medium",
            "title": "Emotional Wellness Support",
            "message": "Your emotional health could benefit from additional support.",
            "action_items": [
                "Practice daily gratitude or journaling",
                "Connect with friends or family regularly",
                "Consider professional support if needed",
                "Engage in activities that bring you joy"
            ]
        })
    
    return insights
