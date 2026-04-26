"""
Sleep prediction and analysis service for EliteHer.
Analyzes sleep patterns, predicts sleep quality, and provides sleep wellness insights.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple
import statistics
import numpy as np
from datetime import datetime


def analyze_sleep_patterns(cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze sleep patterns across menstrual cycles.
    
    Returns:
        - Sleep quality trends
        - Sleep duration patterns
        - Sleep-mood correlations
        - Sleep recommendations
    """
    
    if not cycles:
        return {"patterns": [], "insights": [], "correlations": {}}
    
    sleep_data = []
    for cycle in cycles:
        sleep_hours = cycle.get("sleep_hours")
        if sleep_hours is not None:
            cycle_date = datetime.fromisoformat(cycle.get("start_date", "")[:10])
            sleep_data.append({
                "sleep_hours": sleep_hours,
                "date": cycle_date,
                "mood": cycle.get("mood", "").lower(),
                "symptoms": cycle.get("symptoms", []),
                "stress": cycle.get("stress"),
                "exercise": cycle.get("exercise", "").lower()
            })
    
    if not sleep_data:
        return {"patterns": [], "insights": [], "correlations": {}}
    
    # Sleep duration analysis
    sleep_hours = [entry["sleep_hours"] for entry in sleep_data]
    avg_sleep = statistics.mean(sleep_hours)
    sleep_consistency = 1 - (statistics.stdev(sleep_hours) / avg_sleep) if len(sleep_hours) > 1 else 1
    
    # Sleep quality categorization
    sleep_quality = categorize_sleep_quality(avg_sleep)
    
    # Sleep patterns by cycle phase
    cycle_phase_patterns = analyze_sleep_by_cycle_phase(sleep_data)
    
    # Sleep-mood correlations
    mood_correlations = analyze_sleep_mood_correlations(sleep_data)
    
    # Sleep-stress correlations
    stress_correlations = analyze_sleep_stress_correlations(sleep_data)
    
    # Generate insights
    insights = generate_sleep_insights(avg_sleep, sleep_consistency, cycle_phase_patterns, mood_correlations, stress_correlations)
    
    return {
        "average_sleep_hours": round(avg_sleep, 1),
        "sleep_consistency": round(sleep_consistency, 2),
        "sleep_quality": sleep_quality,
        "cycle_phase_patterns": cycle_phase_patterns,
        "mood_correlations": mood_correlations,
        "stress_correlations": stress_correlations,
        "insights": insights,
        "total_entries": len(sleep_data)
    }


def categorize_sleep_quality(avg_sleep: float) -> str:
    """Categorize sleep quality based on average hours."""
    if 7 <= avg_sleep <= 9:
        return "optimal"
    elif 6 <= avg_sleep < 7 or 9 < avg_sleep <= 10:
        return "good"
    elif 5 <= avg_sleep < 6 or 10 < avg_sleep <= 11:
        return "fair"
    else:
        return "poor"


def analyze_sleep_by_cycle_phase(sleep_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze sleep patterns by menstrual cycle phase."""
    if len(sleep_data) < 3:
        return {"pattern": "insufficient_data", "insights": []}
    
    # Sort by date
    sleep_data.sort(key=lambda x: x["date"])
    
    # Identify cycle phases (simplified approach)
    phase_patterns = {
        "pre_period": [],
        "during_period": [],
        "post_period": [],
        "mid_cycle": []
    }
    
    for i, entry in enumerate(sleep_data):
        # Simple heuristic for phase assignment
        if i == 0:
            phase = "mid_cycle"  # First entry, assume mid-cycle
        else:
            # Check if this might be period (based on cycle length patterns)
            prev_entry = sleep_data[i-1]
            days_diff = (entry["date"] - prev_entry["date"]).days
            
            if days_diff >= 21:  # Likely new cycle starting
                phase = "during_period"
            elif days_diff <= 5:  # Early in cycle
                phase = "post_period"
            elif days_diff <= 15:  # Mid cycle
                phase = "mid_cycle"
            else:  # Pre-period
                phase = "pre_period"
        
        phase_patterns[phase].append(entry["sleep_hours"])
    
    # Calculate averages for each phase
    phase_averages = {}
    for phase, hours_list in phase_patterns.items():
        if hours_list:
            phase_averages[phase] = round(statistics.mean(hours_list), 1)
    
    # Identify patterns
    insights = []
    if len(phase_averages) >= 2:
        max_sleep_phase = max(phase_averages.items(), key=lambda x: x[1])
        min_sleep_phase = min(phase_averages.items(), key=lambda x: x[1])
        
        insights.append(f"You sleep best during {max_sleep_phase[0]} ({max_sleep_phase[1]} hours)")
        insights.append(f"You sleep least during {min_sleep_phase[0]} ({min_sleep_phase[1]} hours)")
        
        # Check for pre-period sleep disruption
        if phase_averages.get("pre_period", 8) < phase_averages.get("mid_cycle", 8) - 1:
            insights.append("Your sleep decreases before your period - plan for extra rest")
    
    return {
        "phase_averages": phase_averages,
        "insights": insights,
        "data_points": {phase: len(hours) for phase, hours in phase_patterns.items()}
    }


def analyze_sleep_mood_correlations(sleep_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze correlations between sleep and mood."""
    mood_sleep_data = {}
    
    for entry in sleep_data:
        mood = entry.get("mood", "")
        sleep = entry.get("sleep_hours")
        
        if mood and sleep is not None:
            if mood not in mood_sleep_data:
                mood_sleep_data[mood] = []
            mood_sleep_data[mood].append(sleep)
    
    correlations = {}
    for mood, sleep_values in mood_sleep_data.items():
        if len(sleep_values) >= 2:
            avg_sleep = statistics.mean(sleep_values)
            correlations[mood] = {
                "average_sleep": round(avg_sleep, 1),
                "sample_size": len(sleep_values),
                "sleep_range": [round(min(sleep_values), 1), round(max(sleep_values), 1)]
            }
    
    return correlations


def analyze_sleep_stress_correlations(sleep_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze correlations between sleep and stress."""
    stress_sleep_pairs = []
    
    for entry in sleep_data:
        stress = entry.get("stress")
        sleep = entry.get("sleep_hours")
        
        if stress is not None and sleep is not None:
            stress_sleep_pairs.append({"stress": stress, "sleep": sleep})
    
    if len(stress_sleep_pairs) < 3:
        return {"correlation": "insufficient_data", "insights": []}
    
    # Calculate correlation
    stress_values = [pair["stress"] for pair in stress_sleep_pairs]
    sleep_values = [pair["sleep"] for pair in stress_sleep_pairs]
    
    correlation = np.corrcoef(stress_values, sleep_values)[0, 1]
    
    insights = []
    if correlation < -0.3:
        insights.append("Higher stress correlates with poorer sleep - focus on stress management")
    elif correlation > 0.3:
        insights.append("Interestingly, higher stress correlates with more sleep - possibly fatigue")
    else:
        insights.append("No strong correlation between stress and sleep in your data")
    
    return {
        "correlation_coefficient": round(correlation, 3),
        "insights": insights,
        "sample_size": len(stress_sleep_pairs)
    }


def generate_sleep_insights(avg_sleep: float, consistency: float, 
                           phase_patterns: Dict[str, Any], mood_correlations: Dict[str, Any], 
                           stress_correlations: Dict[str, Any]) -> List[str]:
    """Generate comprehensive sleep insights."""
    insights = []
    
    # Overall sleep quality
    if 7 <= avg_sleep <= 9:
        insights.append("Your average sleep is optimal for health and wellness")
    elif avg_sleep < 6:
        insights.append("You're not getting enough sleep - this affects mood and health")
    elif avg_sleep > 10:
        insights.append("You're sleeping more than usual - consider sleep quality")
    else:
        insights.append("Your sleep is close to recommended levels")
    
    # Sleep consistency
    if consistency > 0.8:
        insights.append("Excellent sleep consistency - your body thrives on routine")
    elif consistency < 0.5:
        insights.append("Irregular sleep patterns - try to maintain consistent sleep schedule")
    
    # Phase-specific insights
    phase_insights = phase_patterns.get("insights", [])
    insights.extend(phase_insights[:2])  # Add top 2 phase insights
    
    # Mood-sleep insights
    if mood_correlations:
        best_mood_sleep = max(mood_correlations.items(), key=lambda x: x[1]["average_sleep"])
        worst_mood_sleep = min(mood_correlations.items(), key=lambda x: x[1]["average_sleep"])
        
        insights.append(f"You sleep best when feeling {best_mood_sleep[0]} ({best_mood_sleep[1]['average_sleep']} hours)")
        if worst_mood_sleep[0] != best_mood_sleep[0]:
            insights.append(f"Sleep is poorest when feeling {worst_mood_sleep[0]} ({worst_mood_sleep[1]['average_sleep']} hours)")
    
    return insights[:6]  # Return top 6 insights


def predict_sleep_trends(cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Predict sleep trends for the upcoming cycle."""
    if len(cycles) < 3:
        return {"prediction": "insufficient_data", "confidence": 0}
    
    # Get recent sleep data
    recent_cycles = sorted(cycles, key=lambda x: x.get("start_date", ""))[-6:]
    sleep_sequence = []
    
    for cycle in recent_cycles:
        sleep = cycle.get("sleep_hours")
        if sleep is not None:
            sleep_sequence.append(sleep)
    
    if len(sleep_sequence) < 3:
        return {"prediction": "insufficient_data", "confidence": 0}
    
    # Calculate trend
    if len(sleep_sequence) >= 3:
        x = list(range(len(sleep_sequence)))
        trend_slope = np.polyfit(x, sleep_sequence, 1)[0]
        
        # Predict next sleep duration
        next_predicted = sleep_sequence[-1] + trend_slope
        
        # Determine trend direction
        if trend_slope > 0.2:
            trend_direction = "improving"
            message = "Your sleep patterns are improving - keep up the good habits!"
        elif trend_slope < -0.2:
            trend_direction = "declining"
            message = "Your sleep may need attention - focus on sleep hygiene"
        else:
            trend_direction = "stable"
            message = "Your sleep patterns are relatively stable"
        
        # Calculate confidence based on consistency
        if len(sleep_sequence) > 1 and statistics.mean(sleep_sequence) > 0:
            consistency = 1 - (statistics.stdev(sleep_sequence) / statistics.mean(sleep_sequence))
        else:
            consistency = 0
        confidence = max(0, min(1, consistency))
        
        # Categorize predicted sleep
        predicted_quality = categorize_sleep_quality(next_predicted)
        
        return {
            "trend_direction": trend_direction,
            "next_predicted_hours": round(max(0, min(12, next_predicted)), 1),
            "predicted_quality": predicted_quality,
            "message": message,
            "confidence": round(confidence, 2),
            "trend_slope": round(trend_slope, 2),
            "recent_averages": [round(s, 1) for s in sleep_sequence[-3:]],
            "recommendation": get_sleep_prediction_recommendation(predicted_quality, trend_direction)
        }
    
    return {"prediction": "unclear", "confidence": 0}


def get_sleep_prediction_recommendation(quality: str, trend: str) -> str:
    """Get recommendation based on sleep prediction."""
    if trend == "declining":
        return "Focus on sleep hygiene: consistent bedtime, no screens before bed, cool dark room"
    elif trend == "improving":
        return "Great progress! Maintain your current sleep routine and habits"
    else:
        if quality == "optimal":
            return "Excellent sleep patterns! Continue your current routine"
        elif quality == "poor":
            return "Prioritize sleep - aim for 7-9 hours with consistent schedule"
        else:
            return "Good sleep foundation - small improvements could optimize your rest"


def get_sleep_recommendations(current_sleep: float, patterns: Dict[str, Any]) -> List[str]:
    """Get personalized sleep recommendations."""
    recommendations = []
    
    # Based on current sleep duration
    if current_sleep < 6:
        recommendations.extend([
            "Prioritize getting 7-9 hours of sleep per night",
            "Create a relaxing bedtime routine 30 minutes before sleep",
            "Avoid screens and caffeine 2 hours before bedtime",
            "Keep your bedroom cool, dark, and quiet"
        ])
    elif current_sleep > 10:
        recommendations.extend([
            "You may be oversleeping - try to wake up at consistent time",
            "Consider sleep quality over quantity",
            "Check for underlying causes of excessive sleep"
        ])
    else:  # 6-10 hours
        recommendations.extend([
            "Maintain your current sleep duration",
            "Focus on sleep consistency - same bedtime and wake time",
            "Optimize sleep environment for better quality"
        ])
    
    # Based on patterns
    phase_patterns = patterns.get("cycle_phase_patterns", {})
    if phase_patterns.get("insights"):
        for insight in phase_patterns["insights"]:
            if "pre-period" in insight.lower() and "decreases" in insight.lower():
                recommendations.append("Plan for extra rest during the week before your period")
                break
    
    # Based on stress correlations
    stress_corr = patterns.get("stress_correlations", {})
    if stress_corr.get("correlation_coefficient", 0) < -0.3:
        recommendations.append("Manage stress to improve sleep quality")
    
    return recommendations[:4]  # Return top 4 recommendations
