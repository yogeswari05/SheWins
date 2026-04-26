"""
Adaptive confidence scoring system for prediction accuracy.
Dynamically adjusts confidence based on data quality and pattern recognition.
"""
from __future__ import annotations

import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from scipy import stats
from sklearn.metrics import mean_absolute_error, mean_squared_error
import statistics


class AdaptiveConfidenceScorer:
    """Advanced confidence scoring with adaptive algorithms."""
    
    def __init__(self):
        self.confidence_factors = {
            "data_quantity": 0.25,
            "data_quality": 0.20,
            "pattern_consistency": 0.20,
            "prediction_stability": 0.15,
            "historical_accuracy": 0.10,
            "external_factors": 0.10
        }
        
        self.quality_thresholds = {
            "excellent": 0.85,
            "good": 0.70,
            "moderate": 0.55,
            "poor": 0.40,
            "very_poor": 0.25
        }
    
    def calculate_adaptive_confidence(self, 
                                    cycle_lengths: List[int],
                                    predictions: List[Dict[str, Any]],
                                    historical_data: Optional[Dict[str, Any]] = None,
                                    lifestyle_factors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate comprehensive adaptive confidence score."""
        
        if len(cycle_lengths) < 2:
            return self._insufficient_data_confidence()
        
        # Calculate individual confidence factors
        factors = {}
        
        # 1. Data quantity factor
        factors["data_quantity"] = self._calculate_data_quantity_factor(cycle_lengths)
        
        # 2. Data quality factor
        factors["data_quality"] = self._calculate_data_quality_factor(cycle_lengths)
        
        # 3. Pattern consistency factor
        factors["pattern_consistency"] = self._calculate_pattern_consistency_factor(cycle_lengths)
        
        # 4. Prediction stability factor
        factors["prediction_stability"] = self._calculate_prediction_stability_factor(predictions)
        
        # 5. Historical accuracy factor
        factors["historical_accuracy"] = self._calculate_historical_accuracy_factor(historical_data)
        
        # 6. External factors
        factors["external_factors"] = self._calculate_external_factors_factor(lifestyle_factors)
        
        # Calculate weighted confidence
        overall_confidence = self._weighted_confidence(factors)
        
        # Determine confidence tier
        confidence_tier = self._determine_confidence_tier(overall_confidence)
        
        # Generate confidence explanation
        explanation = self._generate_confidence_explanation(factors, overall_confidence, confidence_tier)
        
        # Suggest improvements
        improvements = self._suggest_confidence_improvements(factors, cycle_lengths)
        
        return {
            "overall_confidence": round(overall_confidence, 3),
            "confidence_tier": confidence_tier,
            "individual_factors": factors,
            "explanation": explanation,
            "improvement_suggestions": improvements,
            "reliability_assessment": self._assess_reliability(overall_confidence, factors),
            "prediction_certainty": self._assess_prediction_certainty(overall_confidence, predictions)
        }
    
    def _calculate_data_quantity_factor(self, cycle_lengths: List[int]) -> float:
        """Calculate confidence based on data quantity."""
        n_cycles = len(cycle_lengths)
        
        if n_cycles >= 12:
            return 0.95  # Excellent - seasonal patterns detectable
        elif n_cycles >= 8:
            return 0.85  # Very good - good pattern recognition
        elif n_cycles >= 6:
            return 0.75  # Good - reasonable predictions
        elif n_cycles >= 4:
            return 0.60  # Moderate - basic predictions
        elif n_cycles >= 2:
            return 0.40  # Poor - minimal predictions
        else:
            return 0.10  # Very poor - insufficient data
    
    def _calculate_data_quality_factor(self, cycle_lengths: List[int]) -> float:
        """Calculate confidence based on data quality."""
        if len(cycle_lengths) < 3:
            return 0.5
        
        # Check for data quality issues
        quality_score = 1.0
        
        # Check for outliers
        mean_val = np.mean(cycle_lengths)
        std_val = np.std(cycle_lengths)
        
        outlier_count = 0
        for length in cycle_lengths:
            if abs(length - mean_val) > 3 * std_val:
                outlier_count += 1
        
        # Penalize for outliers
        outlier_penalty = (outlier_count / len(cycle_lengths)) * 0.3
        quality_score -= outlier_penalty
        
        # Check for impossible values
        impossible_count = sum(1 for length in cycle_lengths if length < 15 or length > 90)
        if impossible_count > 0:
            quality_score -= 0.4
        
        # Check for data consistency (no duplicate dates assumed)
        # This would need actual dates, but we'll use cycle length consistency
        if len(cycle_lengths) >= 3:
            # Check for reasonable variance
            cv = std_val / mean_val  # Coefficient of variation
            if cv > 0.5:  # Very high variance
                quality_score -= 0.2
            elif cv > 0.3:  # High variance
                quality_score -= 0.1
        
        return max(0.1, min(1.0, quality_score))
    
    def _calculate_pattern_consistency_factor(self, cycle_lengths: List[int]) -> float:
        """Calculate confidence based on pattern consistency."""
        if len(cycle_lengths) < 4:
            return 0.5
        
        # Calculate pattern consistency metrics
        consistency_score = 0.0
        
        # 1. Regularity score
        if len(cycle_lengths) >= 3:
            std_dev = np.std(cycle_lengths)
            regularity_score = max(0, 1.0 - (std_dev / 15.0))
            consistency_score += regularity_score * 0.4
        
        # 2. Trend consistency
        if len(cycle_lengths) >= 6:
            # Calculate trend in first half vs second half
            mid_point = len(cycle_lengths) // 2
            first_half = cycle_lengths[:mid_point]
            second_half = cycle_lengths[mid_point:]
            
            first_trend = np.polyfit(range(len(first_half)), first_half, 1)[0]
            second_trend = np.polyfit(range(len(second_half)), second_half, 1)[0]
            
            trend_consistency = max(0, 1.0 - abs(first_trend - second_trend) / 5.0)
            consistency_score += trend_consistency * 0.3
        
        # 3. Seasonal pattern detection (if enough data)
        if len(cycle_lengths) >= 12:
            # Simple seasonality check
            seasonal_score = self._detect_seasonality(cycle_lengths)
            consistency_score += seasonal_score * 0.3
        
        return max(0.1, min(1.0, consistency_score))
    
    def _calculate_prediction_stability_factor(self, predictions: List[Dict[str, Any]]) -> float:
        """Calculate confidence based on prediction stability."""
        if not predictions or len(predictions) < 2:
            return 0.5
        
        # Extract prediction values
        pred_values = [p["predicted_length_days"] for p in predictions]
        
        # Calculate prediction variance
        pred_variance = np.var(pred_values)
        pred_mean = np.mean(pred_values)
        
        # Coefficient of variation for predictions
        if pred_mean > 0:
            pred_cv = np.sqrt(pred_variance) / pred_mean
        else:
            pred_cv = 1.0
        
        # Stability score (lower variance = higher stability)
        stability_score = max(0, 1.0 - pred_cv)
        
        # Check for monotonic predictions (often more realistic)
        monotonic_score = 0.0
        if len(pred_values) >= 2:
            increasing = all(pred_values[i] <= pred_values[i+1] for i in range(len(pred_values)-1))
            decreasing = all(pred_values[i] >= pred_values[i+1] for i in range(len(pred_values)-1))
            if increasing or decreasing:
                monotonic_score = 0.2
        
        return min(1.0, stability_score + monotonic_score)
    
    def _calculate_historical_accuracy_factor(self, historical_data: Optional[Dict[str, Any]]) -> float:
        """Calculate confidence based on historical prediction accuracy."""
        if not historical_data:
            return 0.7  # Default moderate confidence
        
        # Extract historical accuracy metrics
        past_predictions = historical_data.get("past_predictions", [])
        actual_values = historical_data.get("actual_values", [])
        
        if not past_predictions or not actual_values or len(past_predictions) != len(actual_values):
            return 0.7
        
        # Calculate historical accuracy metrics
        mae = mean_absolute_error(actual_values, past_predictions)
        mape = np.mean([abs((a - p) / a) for a, p in zip(actual_values, past_predictions) if a != 0])
        
        # Convert to confidence score
        accuracy_score = max(0, 1.0 - mape)
        
        return accuracy_score
    
    def _calculate_external_factors_factor(self, lifestyle_factors: Optional[Dict[str, Any]]) -> float:
        """Calculate confidence based on external lifestyle factors."""
        if not lifestyle_factors:
            return 0.7  # Default moderate confidence
        
        factor_score = 0.7  # Base score
        
        # Stress factor consistency
        stress_consistency = lifestyle_factors.get("stress_consistency", 0.5)
        factor_score += (stress_consistency - 0.5) * 0.2
        
        # Sleep regularity
        sleep_regularity = lifestyle_factors.get("sleep_regularity", 0.5)
        factor_score += (sleep_regularity - 0.5) * 0.1
        
        # Exercise consistency
        exercise_consistency = lifestyle_factors.get("exercise_consistency", 0.5)
        factor_score += (exercise_consistency - 0.5) * 0.1
        
        # Symptom tracking completeness
        symptom_completeness = lifestyle_factors.get("symptom_completeness", 0.5)
        factor_score += (symptom_completeness - 0.5) * 0.1
        
        return max(0.1, min(1.0, factor_score))
    
    def _weighted_confidence(self, factors: Dict[str, float]) -> float:
        """Calculate weighted confidence from individual factors."""
        total_score = 0.0
        total_weight = 0.0
        
        for factor_name, factor_value in factors.items():
            weight = self.confidence_factors.get(factor_name, 0.1)
            total_score += factor_value * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.5
    
    def _determine_confidence_tier(self, confidence: float) -> str:
        """Determine confidence tier based on score."""
        for tier, threshold in self.quality_thresholds.items():
            if confidence >= threshold:
                return tier
        return "very_poor"
    
    def _generate_confidence_explanation(self, factors: Dict[str, float], 
                                       overall: float, tier: str) -> str:
        """Generate human-readable confidence explanation."""
        explanations = []
        
        # Find strongest and weakest factors
        strongest_factor = max(factors.items(), key=lambda x: x[1])
        weakest_factor = min(factors.items(), key=lambda x: x[1])
        
        if overall >= 0.8:
            explanations.append(f"High confidence ({overall:.1%}) due to excellent data quality and consistent patterns.")
        elif overall >= 0.6:
            explanations.append(f"Moderate confidence ({overall:.1%}) with generally reliable predictions.")
        elif overall >= 0.4:
            explanations.append(f"Lower confidence ({overall:.1%}) due to data variability or limited history.")
        else:
            explanations.append(f"Low confidence ({overall:.1%}) - more tracking data needed for reliable predictions.")
        
        # Add factor-specific insights
        if strongest_factor[1] >= 0.8:
            explanations.append(f"Strongest factor: {strongest_factor[0].replace('_', ' ').title()} at {strongest_factor[1]:.1%}.")
        
        if weakest_factor[1] <= 0.4:
            explanations.append(f"Main limitation: {weakest_factor[0].replace('_', ' ').title()} at {weakest_factor[1]:.1%}.")
        
        return " ".join(explanations)
    
    def _suggest_confidence_improvements(self, factors: Dict[str, float], 
                                       cycle_lengths: List[int]) -> List[str]:
        """Suggest improvements to increase confidence."""
        suggestions = []
        
        # Data quantity suggestions
        if factors.get("data_quantity", 0) < 0.7:
            current_count = len(cycle_lengths)
            if current_count < 6:
                suggestions.append(f"Track {6 - current_count} more cycles for significantly better predictions.")
            elif current_count < 12:
                suggestions.append(f"Track {12 - current_count} more cycles to enable seasonal pattern detection.")
        
        # Data quality suggestions
        if factors.get("data_quality", 0) < 0.7:
            suggestions.append("Ensure consistent tracking habits and review any unusual cycle entries.")
        
        # Pattern consistency suggestions
        if factors.get("pattern_consistency", 0) < 0.6:
            suggestions.append("Track additional factors (stress, sleep, exercise) to understand pattern variability.")
        
        # External factors suggestions
        if factors.get("external_factors", 0) < 0.6:
            suggestions.append("Improve lifestyle tracking consistency for more confident predictions.")
        
        return suggestions[:3]  # Return top 3 suggestions
    
    def _assess_reliability(self, confidence: float, factors: Dict[str, float]) -> Dict[str, Any]:
        """Assess overall prediction reliability."""
        if confidence >= 0.8:
            reliability_level = "high"
            reliability_description = "Predictions are highly reliable for planning purposes."
        elif confidence >= 0.6:
            reliability_level = "moderate"
            reliability_description = "Predictions are reasonably reliable but monitor for changes."
        elif confidence >= 0.4:
            reliability_level = "low"
            reliability_description = "Predictions have limited reliability - use as general guidance."
        else:
            reliability_level = "very_low"
            reliability_description = "Predictions are not reliable - need more data."
        
        # Check for any critical issues
        critical_issues = []
        for factor_name, factor_value in factors.items():
            if factor_value < 0.3:
                critical_issues.append(factor_name.replace('_', ' ').title())
        
        return {
            "level": reliability_level,
            "description": reliability_description,
            "critical_issues": critical_issues,
            "suitable_for_planning": confidence >= 0.6
        }
    
    def _assess_prediction_certainty(self, confidence: float, 
                                   predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess certainty of specific predictions."""
        if not predictions:
            return {"certainty_level": "unknown", "message": "No predictions available"}
        
        # Calculate prediction spread
        pred_values = [p["predicted_length_days"] for p in predictions]
        pred_spread = max(pred_values) - min(pred_values)
        
        # Individual prediction certainties
        individual_certainties = []
        for pred in predictions:
            pred_confidence = pred.get("confidence", confidence)
            individual_certainties.append({
                "cycle_index": pred["cycle_index"],
                "certainty": pred_confidence,
                "certainty_level": self._determine_confidence_tier(pred_confidence)
            })
        
        # Overall certainty assessment
        if confidence >= 0.8 and pred_spread < 5:
            certainty_level = "high"
            message = "High certainty with consistent predictions across cycles."
        elif confidence >= 0.6 and pred_spread < 10:
            certainty_level = "moderate"
            message = "Moderate certainty with reasonable prediction consistency."
        else:
            certainty_level = "low"
            message = "Lower certainty with significant prediction variation."
        
        return {
            "certainty_level": certainty_level,
            "message": message,
            "prediction_spread": round(pred_spread, 1),
            "individual_certainties": individual_certainties
        }
    
    def _detect_seasonality(self, cycle_lengths: List[int]) -> float:
        """Simple seasonality detection."""
        if len(cycle_lengths) < 12:
            return 0.0
        
        # Calculate seasonal indices
        seasonal_indices = []
        for i in range(12):
            values = [cycle_lengths[j] for j in range(i, len(cycle_lengths), 12)]
            if values:
                seasonal_indices.append(np.mean(values))
        
        if len(seasonal_indices) < 4:
            return 0.0
        
        # Calculate seasonal variance
        seasonal_var = np.var(seasonal_indices)
        overall_var = np.var(cycle_lengths)
        
        if overall_var > 0:
            seasonal_strength = seasonal_var / overall_var
            return min(1.0, seasonal_strength)
        
        return 0.0
    
    def _insufficient_data_confidence(self) -> Dict[str, Any]:
        """Return confidence assessment for insufficient data."""
        return {
            "overall_confidence": 0.1,
            "confidence_tier": "very_poor",
            "explanation": "Insufficient data for reliable predictions. Continue tracking to improve accuracy.",
            "improvement_suggestions": ["Track at least 2-3 more cycles to enable basic predictions"],
            "reliability_assessment": {
                "level": "very_low",
                "description": "Predictions are not reliable - need more data.",
                "suitable_for_planning": False
            }
        }


# Global adaptive confidence scorer instance
adaptive_confidence_scorer = AdaptiveConfidenceScorer()
