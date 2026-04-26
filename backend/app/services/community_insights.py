"""
Community insights service for anonymous peer comparisons and shared experiences.
Helps users feel connected and understand their health patterns in context.
"""
from __future__ import annotations

import statistics
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

from app.services import db


class CommunityInsightsService:
    def __init__(self):
        pass
    
    def get_anonymous_insights(self, user_id: str) -> Dict[str, Any]:
        """Get anonymous community insights for user comparison."""
        cycles = db.list_cycles(user_id)
        
        if not cycles:
            return {
                "message": "Start tracking to see community insights!",
                "insights": {}
            }
        
        # Get user's stats
        user_stats = self._calculate_user_stats(cycles)
        
        # Get community stats (mock data for demo, would aggregate from all users in production)
        community_stats = self._get_community_stats()
        
        # Generate insights
        insights = {
            "cycle_length": self._compare_cycle_length(user_stats, community_stats),
            "symptoms": self._compare_symptoms(user_stats, community_stats),
            "stress": self._compare_stress(user_stats, community_stats),
            "patterns": self._identify_patterns(user_stats),
            "community_support": self._get_support_messages(user_stats)
        }
        
        return {
            "user_stats": user_stats,
            "community_averages": community_stats,
            "insights": insights,
            "disclaimer": "All community data is anonymous and aggregated for privacy."
        }
    
    def _calculate_user_stats(self, cycles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate user's personal statistics."""
        if not cycles:
            return {}
        
        # Cycle lengths
        lengths = []
        for i in range(1, len(cycles)):
            try:
                prev_start = date.fromisoformat(cycles[i-1]["start_date"])
                curr_start = date.fromisoformat(cycles[i]["start_date"])
                length = (curr_start - prev_start).days
                lengths.append(length)
            except (ValueError, KeyError):
                continue
        
        # Symptoms frequency
        symptom_counts = {}
        total_symptoms = 0
        for cycle in cycles:
            symptoms = cycle.get("symptoms", [])
            if isinstance(symptoms, list):
                total_symptoms += len(symptoms)
                for symptom in symptoms:
                    symptom_counts[symptom] = symptom_counts.get(symptom, 0) + 1
        
        # Stress levels
        stress_levels = [cycle.get("stress") for cycle in cycles if cycle.get("stress") is not None]
        
        # Sleep patterns
        sleep_hours = [cycle.get("sleep_hours") for cycle in cycles if cycle.get("sleep_hours") is not None]
        
        # Exercise frequency
        exercise_counts = {}
        for cycle in cycles:
            exercise = cycle.get("exercise", "none")
            exercise_counts[exercise] = exercise_counts.get(exercise, 0) + 1
        
        return {
            "total_cycles": len(cycles),
            "avg_cycle_length": statistics.mean(lengths) if lengths else 0,
            "cycle_length_std": statistics.stdev(lengths) if len(lengths) > 1 else 0,
            "most_common_symptoms": sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "avg_symptoms_per_cycle": total_symptoms / len(cycles) if cycles else 0,
            "avg_stress": statistics.mean(stress_levels) if stress_levels else 0,
            "avg_sleep": statistics.mean(sleep_hours) if sleep_hours else 0,
            "exercise_pattern": exercise_counts,
            "tracking_consistency": self._calculate_consistency(cycles)
        }
    
    def _get_community_stats(self) -> Dict[str, Any]:
        """Get community statistics (mock data for demo)."""
        return {
            "avg_cycle_length": 28.5,
            "cycle_length_std": 3.2,
            "most_common_symptoms": [
                ("cramps", 75),
                ("bloating", 68),
                ("headache", 52),
                ("fatigue", 48),
                ("breast_tenderness", 45)
            ],
            "avg_symptoms_per_cycle": 4.2,
            "avg_stress": 4.8,
            "avg_sleep": 7.1,
            "exercise_pattern": {
                "moderate": 45,
                "light": 30,
                "none": 15,
                "heavy": 10
            },
            "pcod_risk_distribution": {
                "low": 60,
                "medium": 25,
                "high": 15
            }
        }
    
    def _compare_cycle_length(self, user_stats: Dict[str, Any], community_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Compare user's cycle length with community."""
        user_avg = user_stats.get("avg_cycle_length", 0)
        community_avg = community_stats.get("avg_cycle_length", 28.5)
        
        difference = user_avg - community_avg
        
        if abs(difference) <= 2:
            category = "typical"
            message = f"Your cycle length ({user_avg:.1f} days) is very typical for the community!"
        elif difference > 5:
            category = "longer"
            message = f"Your cycles are longer than average ({user_avg:.1f} vs {community_avg:.1f} days)"
        elif difference < -5:
            category = "shorter"
            message = f"Your cycles are shorter than average ({user_avg:.1f} vs {community_avg:.1f} days)"
        else:
            category = "slight_variation"
            message = f"Your cycle length varies slightly from average ({user_avg:.1f} vs {community_avg:.1f} days)"
        
        return {
            "category": category,
            "message": message,
            "user_avg": user_avg,
            "community_avg": community_avg,
            "difference": difference
        }
    
    def _compare_symptoms(self, user_stats: Dict[str, Any], community_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Compare user's symptoms with community."""
        user_symptoms = dict(user_stats.get("most_common_symptoms", []))
        community_symptoms = dict(community_stats.get("most_common_symptoms", []))
        
        user_avg_symptoms = user_stats.get("avg_symptoms_per_cycle", 0)
        community_avg_symptoms = community_stats.get("avg_symptoms_per_cycle", 4.2)
        
        # Find unique symptoms
        user_unique = set(user_symptoms.keys()) - set(community_symptoms.keys())
        community_common = set(community_symptoms.keys()) & set(user_symptoms.keys())
        
        return {
            "avg_symptoms_comparison": {
                "user": user_avg_symptoms,
                "community": community_avg_symptoms,
                "category": "typical" if abs(user_avg_symptoms - community_avg_symptoms) <= 1 else "atypical"
            },
            "shared_symptoms": list(community_common)[:3],
            "unique_symptoms": list(user_unique)[:3],
            "insight": self._get_symptom_insight(user_avg_symptoms, community_avg_symptoms)
        }
    
    def _compare_stress(self, user_stats: Dict[str, Any], community_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Compare user's stress with community."""
        user_stress = user_stats.get("avg_stress", 0)
        community_stress = community_stats.get("avg_stress", 4.8)
        
        if user_stress == 0:
            return {
                "message": "Start tracking stress to see community comparisons!",
                "category": "no_data"
            }
        
        difference = user_stress - community_stress
        
        if abs(difference) <= 1:
            category = "typical"
            message = f"Your stress level ({user_stress:.1f}) is similar to community average"
        elif difference > 2:
            category = "higher"
            message = f"Your stress is higher than average ({user_stress:.1f} vs {community_stress:.1f})"
        elif difference < -2:
            category = "lower"
            message = f"Your stress is lower than average ({user_stress:.1f} vs {community_stress:.1f})"
        else:
            category = "slight_variation"
            message = f"Your stress varies slightly from average ({user_stress:.1f} vs {community_stress:.1f})"
        
        return {
            "category": category,
            "message": message,
            "user_stress": user_stress,
            "community_stress": community_stress,
            "recommendation": self._get_stress_recommendation(category)
        }
    
    def _identify_patterns(self, user_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify patterns in user's data."""
        patterns = []
        
        # Regular cycle pattern
        cycle_std = user_stats.get("cycle_length_std", 0)
        if cycle_std < 3:
            patterns.append({
                "type": "regular_cycle",
                "message": "You have very regular cycles - that's great for predictability!",
                "positive": True
            })
        elif cycle_std > 8:
            patterns.append({
                "type": "irregular_cycle",
                "message": "Your cycles vary quite a bit - consider tracking more details",
                "positive": False
            })
        
        # High symptom awareness
        avg_symptoms = user_stats.get("avg_symptoms_per_cycle", 0)
        if avg_symptoms >= 5:
            patterns.append({
                "type": "symptom_aware",
                "message": "You're very aware of your symptoms - this helps with pattern recognition!",
                "positive": True
            })
        
        # Stress management
        avg_stress = user_stats.get("avg_stress", 0)
        if avg_stress > 0 and avg_stress <= 3:
            patterns.append({
                "type": "good_stress_management",
                "message": "Your stress levels are well managed - keep it up!",
                "positive": True
            })
        elif avg_stress >= 7:
            patterns.append({
                "type": "high_stress",
                "message": "Your stress levels are consistently high - consider stress management techniques",
                "positive": False
            })
        
        return patterns
    
    def _get_support_messages(self, user_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get personalized support messages."""
        messages = []
        
        # Based on cycle regularity
        cycle_std = user_stats.get("cycle_length_std", 0)
        if cycle_std > 5:
            messages.append({
                "type": "support",
                "title": "You're Not Alone",
                "message": "Many people experience irregular cycles. Consistent tracking helps identify patterns.",
                "action": "Continue tracking and consider discussing with a healthcare provider"
            })
        
        # Based on symptoms
        avg_symptoms = user_stats.get("avg_symptoms_per_cycle", 0)
        if avg_symptoms >= 6:
            messages.append({
                "type": "validation",
                "title": "Your Experience Matters",
                "message": "Tracking multiple symptoms shows great self-awareness. This information is valuable for understanding your health.",
                "action": "Keep up the detailed tracking - it makes a difference!"
            })
        
        # General encouragement
        total_cycles = user_stats.get("total_cycles", 0)
        if total_cycles >= 6:
            messages.append({
                "type": "achievement",
                "title": "Health Tracking Champion",
                "message": f"You've tracked {total_cycles} cycles! This consistency helps you understand your body better.",
                "action": "You're building a valuable health record"
            })
        
        return messages
    
    def _calculate_consistency(self, cycles: List[Dict[str, Any]]) -> float:
        """Calculate tracking consistency score."""
        if not cycles:
            return 0.0
        
        complete_cycles = 0
        for cycle in cycles:
            required_fields = ["start_date", "flow"]
            if all(cycle.get(field) for field in required_fields):
                complete_cycles += 1
        
        return (complete_cycles / len(cycles)) * 100
    
    def _get_symptom_insight(self, user_avg: float, community_avg: float) -> str:
        """Get insight about symptom tracking."""
        if user_avg > community_avg + 2:
            return "You're very in tune with your body - great symptom awareness!"
        elif user_avg < community_avg - 2:
            return "Consider tracking more symptoms to identify patterns"
        else:
            return "Your symptom tracking is similar to others in the community"
    
    def _get_stress_recommendation(self, category: str) -> str:
        """Get stress management recommendation."""
        recommendations = {
            "higher": "Try meditation, gentle exercise, or talking with friends",
            "lower": "Great job managing stress! Share your techniques with others",
            "typical": "Continue your current stress management routine",
            "slight_variation": "Small adjustments to your routine might help"
        }
        return recommendations.get(category, "Focus on self-care and stress awareness")


# Global service instance
community_insights_service = CommunityInsightsService()
