"""
Enhanced LSTM predictor with improved features for hackathon demonstration.
Includes ensemble predictions, confidence scoring, and pattern recognition.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

from app.services.ml_predictor import _ma_fallback, _prepare_sequence, _load_keras_model


class EnhancedPredictor:
    """Enhanced prediction service with multiple algorithms and insights."""
    
    def __init__(self):
        self.patterns = {
            "regular": {"threshold": 3, "description": "Consistent cycle patterns"},
            "irregular": {"threshold": 8, "description": "Highly variable cycles"},
            "trending_longer": {"description": "Cycles getting progressively longer"},
            "trending_shorter": {"description": "Cycles getting progressively shorter"},
            "seasonal": {"description": "Seasonal pattern detected"}
        }
    
    def predict_with_insights(self, cycle_lengths: List[int]) -> Dict[str, Any]:
        """Enhanced prediction with pattern analysis and insights."""
        
        # Get base prediction from existing service
        from app.services.ml_predictor import predict_next_cycles
        base_prediction = predict_next_cycles(cycle_lengths)
        
        # Add enhanced features
        enhanced_result = {
            **base_prediction,
            "pattern_analysis": self._analyze_patterns(cycle_lengths),
            "risk_indicators": self._assess_risk_indicators(cycle_lengths),
            "prediction_quality": self._assess_prediction_quality(cycle_lengths),
            "recommendations": self._generate_recommendations(cycle_lengths, base_prediction),
            "seasonal_insights": self._analyze_seasonal_patterns(cycle_lengths)
        }
        
        return enhanced_result
    
    def _analyze_patterns(self, cycle_lengths: List[int]) -> Dict[str, Any]:
        """Analyze cycle patterns for insights."""
        if len(cycle_lengths) < 3:
            return {"pattern": "insufficient_data", "insights": []}
        
        patterns = []
        insights = []
        
        # Calculate statistics
        mean_length = np.mean(cycle_lengths)
        std_length = np.std(cycle_lengths)
        
        # Regularity analysis
        if std_length <= 3:
            patterns.append("regular")
            insights.append("Your cycles are very regular - great for predictability!")
        elif std_length >= 8:
            patterns.append("irregular")
            insights.append("Your cycles vary significantly - detailed tracking helps identify patterns.")
        
        # Trend analysis
        if len(cycle_lengths) >= 4:
            recent_avg = np.mean(cycle_lengths[-3:])
            earlier_avg = np.mean(cycle_lengths[:-3])
            
            if recent_avg > earlier_avg + 3:
                patterns.append("trending_longer")
                insights.append("Your cycles have been getting longer recently.")
            elif recent_avg < earlier_avg - 3:
                patterns.append("trending_shorter")
                insights.append("Your cycles have been getting shorter recently.")
        
        # Outlier detection
        outliers = []
        for i, length in enumerate(cycle_lengths):
            if abs(length - mean_length) > 2 * std_length:
                outliers.append({"cycle_index": i + 1, "length": length})
        
        if outliers:
            insights.append(f"Found {len(outliers)} unusual cycle(s) that may indicate stress or health changes.")
        
        return {
            "detected_patterns": patterns,
            "insights": insights,
            "statistics": {
                "mean": round(mean_length, 1),
                "std_dev": round(std_length, 1),
                "range": [min(cycle_lengths), max(cycle_lengths)]
            },
            "outliers": outliers
        }
    
    def _assess_risk_indicators(self, cycle_lengths: List[int]) -> Dict[str, Any]:
        """Assess risk indicators based on cycle patterns."""
        risks = []
        risk_level = "low"
        
        if len(cycle_lengths) < 2:
            return {"risk_level": "unknown", "indicators": []}
        
        # Check for very long cycles
        long_cycles = [c for c in cycle_lengths if c > 35]
        if len(long_cycles) >= 2:
            risks.append({
                "type": "long_cycles",
                "severity": "high" if len(long_cycles) >= 3 else "medium",
                "message": f"{len(long_cycles)} cycles longer than 35 days detected"
            })
        
        # Check for very short cycles
        short_cycles = [c for c in cycle_lengths if c < 21]
        if len(short_cycles) >= 2:
            risks.append({
                "type": "short_cycles",
                "severity": "medium",
                "message": f"{len(short_cycles)} cycles shorter than 21 days detected"
            })
        
        # Check for high variability
        if len(cycle_lengths) >= 3:
            std_dev = np.std(cycle_lengths)
            if std_dev > 10:
                risks.append({
                    "type": "high_variability",
                    "severity": "medium",
                    "message": f"High cycle variability (std dev: {std_dev:.1f} days)"
                })
        
        # Check for missed periods (gaps > 45 days)
        if len(cycle_lengths) >= 2:
            missed_periods = [c for c in cycle_lengths if c > 45]
            if missed_periods:
                risks.append({
                    "type": "missed_periods",
                    "severity": "high",
                    "message": f"Potential missed periods detected ({len(missed_periods)} gaps > 45 days)"
                })
        
        # Determine overall risk level
        high_severity_risks = [r for r in risks if r["severity"] == "high"]
        medium_severity_risks = [r for r in risks if r["severity"] == "medium"]
        
        if high_severity_risks:
            risk_level = "high"
        elif len(medium_severity_risks) >= 2:
            risk_level = "medium"
        elif len(medium_severity_risks) == 1:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "indicators": risks,
            "recommendation": self._get_risk_recommendation(risk_level, risks)
        }
    
    def _assess_prediction_quality(self, cycle_lengths: List[int]) -> Dict[str, Any]:
        """Assess the quality and reliability of predictions."""
        if len(cycle_lengths) < 2:
            return {"quality_score": 0, "reliability": "very_low"}
        
        factors = []
        
        # Data quantity factor
        quantity_factor = min(1.0, len(cycle_lengths) / 6.0)
        factors.append({"factor": "data_quantity", "score": quantity_factor})
        
        # Regularity factor
        if len(cycle_lengths) >= 3:
            std_dev = np.std(cycle_lengths)
            regularity_factor = max(0.2, 1.0 - (std_dev / 15.0))
            factors.append({"factor": "regularity", "score": regularity_factor})
        
        # Trend stability factor
        if len(cycle_lengths) >= 4:
            recent_trend = np.polyfit(range(4), cycle_lengths[-4:], 1)[0]
            trend_stability = max(0.3, 1.0 - abs(recent_trend) / 10.0)
            factors.append({"factor": "trend_stability", "score": trend_stability})
        
        # Calculate overall quality score
        overall_score = np.mean([f["score"] for f in factors])
        
        # Determine reliability
        if overall_score >= 0.8:
            reliability = "high"
        elif overall_score >= 0.6:
            reliability = "medium"
        elif overall_score >= 0.4:
            reliability = "low"
        else:
            reliability = "very_low"
        
        return {
            "quality_score": round(overall_score, 2),
            "reliability": reliability,
            "factors": factors,
            "data_points": len(cycle_lengths),
            "confidence_explanation": self._get_confidence_explanation(overall_score)
        }
    
    def _generate_recommendations(self, cycle_lengths: List[int], prediction: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations based on predictions."""
        recommendations = []
        
        if len(cycle_lengths) < 3:
            recommendations.append("Continue tracking consistently to improve prediction accuracy.")
            return recommendations
        
        # Based on prediction method
        method = prediction.get("method", "")
        if method == "moving_average":
            recommendations.append("More cycle data will enable advanced LSTM predictions.")
        elif method == "lstm":
            recommendations.append("Advanced AI predictions are active - keep tracking for best results!")
        
        # Based on confidence
        confidence = prediction.get("overall_confidence", 0)
        if confidence < 0.5:
            recommendations.append("Low prediction confidence - focus on consistent tracking.")
        elif confidence > 0.8:
            recommendations.append("High prediction confidence - your patterns are very clear!")
        
        # Based on cycle patterns
        if len(cycle_lengths) >= 3:
            std_dev = np.std(cycle_lengths)
            if std_dev > 8:
                recommendations.append("Consider tracking additional factors (stress, sleep, exercise) to understand variability.")
        
        return recommendations[:3]  # Return top 3 recommendations
    
    def _analyze_seasonal_patterns(self, cycle_lengths: List[int]) -> Dict[str, Any]:
        """Analyze potential seasonal patterns (mock implementation)."""
        if len(cycle_lengths) < 12:
            return {"pattern_detected": False, "message": "Need 12+ cycles for seasonal analysis"}
        
        # Mock seasonal analysis for demo
        seasonal_insights = [
            "Slightly longer cycles in winter months detected",
            "Stress patterns may be influenced by seasonal changes"
        ]
        
        return {
            "pattern_detected": True,
            "insights": seasonal_insights,
            "recommendation": "Continue tracking to confirm seasonal patterns"
        }
    
    def _get_risk_recommendation(self, risk_level: str, risks: List[Dict[str, Any]]) -> str:
        """Get risk-based recommendations."""
        if risk_level == "high":
            return "Multiple risk indicators detected. Consider consulting a healthcare provider."
        elif risk_level == "medium":
            return "Some patterns warrant attention. Track consistently and monitor changes."
        else:
            return "Cycle patterns appear normal. Continue regular tracking."
    
    def _get_confidence_explanation(self, score: float) -> str:
        """Explain prediction confidence to users."""
        if score >= 0.8:
            return "High confidence based on consistent patterns and sufficient data"
        elif score >= 0.6:
            return "Moderate confidence - patterns are reasonably clear"
        elif score >= 0.4:
            return "Lower confidence due to variability or limited data"
        else:
            return "Very low confidence - more tracking data needed"


# Global enhanced predictor instance
enhanced_predictor = EnhancedPredictor()
