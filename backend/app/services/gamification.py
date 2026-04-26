"""
Gamification service for EliteHer - makes health tracking engaging and rewarding.
Includes achievements, points, badges, streaks, and wellness scores.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from app.services import db


# Achievement definitions
ACHIEVEMENTS = {
    "first_cycle": {
        "name": "Cycle Starter",
        "description": "Logged your first period",
        "points": 10,
        "icon": "🌸",
        "category": "milestone"
    },
    "week_streak": {
        "name": "Week Warrior",
        "description": "7 days of consistent tracking",
        "points": 50,
        "icon": "🔥",
        "category": "consistency"
    },
    "month_streak": {
        "name": "Monthly Master",
        "description": "30 days of consistent tracking",
        "points": 200,
        "icon": "💎",
        "category": "consistency"
    },
    "symptom_explorer": {
        "name": "Symptom Detective",
        "description": "Logged 10 different symptoms",
        "points": 30,
        "icon": "🔍",
        "category": "exploration"
    },
    "mood_tracker": {
        "name": "Emotion Explorer",
        "description": "Tracked mood for 10 cycles",
        "points": 25,
        "icon": "😊",
        "category": "wellness"
    },
    "stress_aware": {
        "name": "Stress Guru",
        "description": "Analyzed stress levels 5 times",
        "points": 40,
        "icon": "🧘",
        "category": "wellness"
    },
    "pcod_informed": {
        "name": "Health Aware",
        "description": "Completed PCOD risk assessment",
        "points": 35,
        "icon": "🩺",
        "category": "health"
    },
    "data_lover": {
        "name": "Data Diva",
        "description": "Logged 20+ data points in one cycle",
        "points": 45,
        "icon": "📊",
        "category": "comprehensive"
    },
    "prediction_pro": {
        "name": "Future Seer",
        "description": "Used cycle prediction feature",
        "points": 30,
        "icon": "🔮",
        "category": "advanced"
    },
    "wellness_warrior": {
        "name": "Wellness Champion",
        "description": "Maintained wellness score above 80 for a month",
        "points": 100,
        "icon": "🏆",
        "category": "elite"
    }
}


class GamificationService:
    def __init__(self):
        self.achievements = ACHIEVEMENTS
    
    def calculate_wellness_score(self, user_id: str) -> Dict[str, Any]:
        """Calculate comprehensive wellness score (0-100) based on multiple factors."""
        cycles = db.list_cycles(user_id)
        
        if not cycles:
            return {
                "score": 0,
                "level": "newbie",
                "factors": {},
                "recommendations": ["Start tracking your cycles to see your wellness score!"]
            }
        
        # Factor 1: Cycle Regularity (25%)
        regularity_score = self._calculate_regularity_score(cycles)
        
        # Factor 2: Symptom Awareness (20%)
        symptom_score = self._calculate_symptom_score(cycles)
        
        # Factor 3: Lifestyle Tracking (25%)
        lifestyle_score = self._calculate_lifestyle_score(cycles)
        
        # Factor 4: Stress Management (15%)
        stress_score = self._calculate_stress_management_score(cycles)
        
        # Factor 5: Consistency (15%)
        consistency_score = self._calculate_consistency_score(cycles)
        
        # Calculate weighted total
        total_score = (
            regularity_score * 0.25 +
            symptom_score * 0.20 +
            lifestyle_score * 0.25 +
            stress_score * 0.15 +
            consistency_score * 0.15
        )
        
        # Determine level
        if total_score >= 90:
            level = "elite"
            level_desc = "Wellness Master"
        elif total_score >= 75:
            level = "advanced"
            level_desc = "Health Hero"
        elif total_score >= 60:
            level = "intermediate"
            level_desc = "Wellness Warrior"
        elif total_score >= 40:
            level = "beginner"
            level_desc = "Health Explorer"
        else:
            level = "newbie"
            level_desc = "Just Starting"
        
        return {
            "score": round(total_score, 1),
            "level": level,
            "level_description": level_desc,
            "factors": {
                "regularity": round(regularity_score, 1),
                "symptoms": round(symptom_score, 1),
                "lifestyle": round(lifestyle_score, 1),
                "stress": round(stress_score, 1),
                "consistency": round(consistency_score, 1)
            },
            "recommendations": self._get_wellness_recommendations(total_score, {
                "regularity": regularity_score,
                "symptoms": symptom_score,
                "lifestyle": lifestyle_score,
                "stress": stress_score,
                "consistency": consistency_score
            })
        }
    
    def _calculate_regularity_score(self, cycles: List[Dict[str, Any]]) -> float:
        """Calculate cycle regularity score."""
        if len(cycles) < 2:
            return 30.0  # Base score for insufficient data
        
        # Calculate cycle lengths
        lengths = []
        for i in range(1, len(cycles)):
            try:
                prev_start = date.fromisoformat(cycles[i-1]["start_date"])
                curr_start = date.fromisoformat(cycles[i]["start_date"])
                length = (curr_start - prev_start).days
                lengths.append(length)
            except (ValueError, KeyError):
                continue
        
        if not lengths:
            return 30.0
        
        avg_length = sum(lengths) / len(lengths)
        variance = sum((x - avg_length) ** 2 for x in lengths) / len(lengths)
        std_dev = variance ** 0.5
        
        # Score based on regularity (lower std_dev = higher score)
        if std_dev <= 2:
            return 100.0
        elif std_dev <= 4:
            return 85.0
        elif std_dev <= 7:
            return 70.0
        elif std_dev <= 10:
            return 55.0
        elif std_dev <= 15:
            return 40.0
        else:
            return 25.0
    
    def _calculate_symptom_score(self, cycles: List[Dict[str, Any]]) -> float:
        """Calculate symptom tracking score."""
        total_symptoms = 0
        cycles_with_symptoms = 0
        
        for cycle in cycles:
            symptoms = cycle.get("symptoms", [])
            if isinstance(symptoms, list) and symptoms:
                cycles_with_symptoms += 1
                total_symptoms += len(symptoms)
        
        if not cycles:
            return 0.0
        
        symptom_coverage = cycles_with_symptoms / len(cycles)
        avg_symptoms_per_cycle = total_symptoms / max(1, cycles_with_symptoms)
        
        # Score based on coverage and detail
        coverage_score = symptom_coverage * 50
        detail_score = min(50, avg_symptoms_per_cycle * 5)
        
        return coverage_score + detail_score
    
    def _calculate_lifestyle_score(self, cycles: List[Dict[str, Any]]) -> float:
        """Calculate lifestyle tracking score."""
        sleep_tracked = 0
        exercise_tracked = 0
        mood_tracked = 0
        
        for cycle in cycles:
            if cycle.get("sleep_hours") is not None:
                sleep_tracked += 1
            if cycle.get("exercise"):
                exercise_tracked += 1
            if cycle.get("mood"):
                mood_tracked += 1
        
        if not cycles:
            return 0.0
        
        total_possible = len(cycles) * 3
        total_tracked = sleep_tracked + exercise_tracked + mood_tracked
        
        return (total_tracked / total_possible) * 100
    
    def _calculate_stress_management_score(self, cycles: List[Dict[str, Any]]) -> float:
        """Calculate stress management score."""
        stress_tracked = 0
        low_stress_cycles = 0
        
        for cycle in cycles:
            stress = cycle.get("stress")
            if stress is not None:
                stress_tracked += 1
                if stress <= 5:
                    low_stress_cycles += 1
        
        if not cycles:
            return 0.0
        
        tracking_score = (stress_tracked / len(cycles)) * 50
        management_score = (low_stress_cycles / max(1, stress_tracked)) * 50 if stress_tracked > 0 else 0
        
        return tracking_score + management_score
    
    def _calculate_consistency_score(self, cycles: List[Dict[str, Any]]) -> float:
        """Calculate tracking consistency score."""
        if not cycles:
            return 0.0
        
        # Check for data completeness in recent cycles
        recent_cycles = cycles[-6:]  # Last 6 cycles
        complete_cycles = 0
        
        for cycle in recent_cycles:
            required_fields = ["start_date", "flow"]
            optional_fields = ["symptoms", "mood", "sleep_hours", "stress", "exercise"]
            
            has_required = all(cycle.get(field) for field in required_fields)
            has_optional = sum(1 for field in optional_fields if cycle.get(field))
            
            if has_required and has_optional >= 3:
                complete_cycles += 1
        
        return (complete_cycles / len(recent_cycles)) * 100
    
    def _get_wellness_recommendations(self, total_score: float, factors: Dict[str, float]) -> List[str]:
        """Get personalized recommendations based on wellness analysis."""
        recommendations = []
        
        if total_score < 50:
            recommendations.append("Keep tracking consistently to improve your wellness score!")
        
        if factors["regularity"] < 60:
            recommendations.append("Focus on consistent cycle timing for better regularity insights.")
        
        if factors["symptoms"] < 50:
            recommendations.append("Try to log symptoms more consistently - it helps identify patterns!")
        
        if factors["lifestyle"] < 60:
            recommendations.append("Add sleep, exercise, and mood tracking for better wellness insights.")
        
        if factors["stress"] < 50:
            recommendations.append("Track stress levels and try relaxation techniques.")
        
        if factors["consistency"] < 70:
            recommendations.append("Complete more fields in your cycle entries for better analysis.")
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def check_achievements(self, user_id: str) -> Dict[str, Any]:
        """Check and unlock achievements for a user."""
        cycles = db.list_cycles(user_id)
        unlocked_achievements = []
        
        # First cycle
        if cycles:
            unlocked_achievements.append("first_cycle")
        
        # Symptom explorer
        all_symptoms = set()
        for cycle in cycles:
            symptoms = cycle.get("symptoms", [])
            if isinstance(symptoms, list):
                all_symptoms.update(symptoms)
        
        if len(all_symptoms) >= 10:
            unlocked_achievements.append("symptom_explorer")
        
        # Mood tracker
        mood_cycles = sum(1 for cycle in cycles if cycle.get("mood"))
        if mood_cycles >= 10:
            unlocked_achievements.append("mood_tracker")
        
        # Data lover
        for cycle in cycles:
            data_points = 0
            if cycle.get("symptoms"):
                data_points += len(cycle["symptoms"])
            if cycle.get("mood"):
                data_points += 1
            if cycle.get("sleep_hours"):
                data_points += 1
            if cycle.get("stress"):
                data_points += 1
            if cycle.get("exercise"):
                data_points += 1
            if cycle.get("notes"):
                data_points += 1
            
            if data_points >= 20:
                unlocked_achievements.append("data_lover")
                break
        
        # Calculate total points
        total_points = sum(
            self.achievements[achievement]["points"] 
            for achievement in unlocked_achievements
            if achievement in self.achievements
        )
        
        return {
            "unlocked": unlocked_achievements,
            "total_points": total_points,
            "achievement_details": [
                {
                    "id": achievement,
                    **self.achievements[achievement]
                }
                for achievement in unlocked_achievements
                if achievement in self.achievements
            ]
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get wellness leaderboard (mock implementation for demo)."""
        # In a real implementation, this would aggregate across all users
        # For demo purposes, return mock data
        return [
            {"rank": 1, "name": "Wellness Queen", "score": 95.2, "level": "elite"},
            {"rank": 2, "name": "Health Hero", "score": 88.7, "level": "advanced"},
            {"rank": 3, "name": "Cycle Master", "score": 82.1, "level": "advanced"},
            {"rank": 4, "name": "Symptom Sleuth", "score": 76.4, "level": "intermediate"},
            {"rank": 5, "name": "Stress Guru", "score": 71.8, "level": "intermediate"},
        ]


# Global service instance
gamification_service = GamificationService()
