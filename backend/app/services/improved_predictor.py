"""
Improved prediction service integrating ensemble methods, feature engineering,
and adaptive confidence scoring for enhanced accuracy.
"""
from __future__ import annotations

import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timedelta

from app.services.ensemble_predictor import ensemble_predictor
from app.services.feature_engineer import feature_engineer
from app.services.adaptive_confidence import adaptive_confidence_scorer
from app.services.ml_predictor import predict_next_cycles
from app.services.enhanced_predictor import enhanced_predictor


class ImprovedPredictor:
    """Next-generation prediction service with maximum accuracy."""
    
    def __init__(self):
        self.ensemble_predictor = ensemble_predictor
        self.feature_engineer = feature_engineer
        self.confidence_scorer = adaptive_confidence_scorer
        self.enhanced_predictor = enhanced_predictor
        
        # Prediction method selection logic
        self.method_thresholds = {
            "ensemble": 8,      # Use ensemble for 8+ cycles
            "enhanced": 4,      # Use enhanced for 4+ cycles
            "basic": 2          # Use basic for 2+ cycles
        }
    
    def predict_with_maximum_accuracy(self, 
                                     cycle_lengths: List[int],
                                     cycle_data: Optional[List[Dict[str, Any]]] = None,
                                     user_preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate predictions with maximum possible accuracy using all available methods.
        """
        
        if len(cycle_lengths) < 2:
            return self._insufficient_data_response()
        
        # Select optimal prediction method
        method = self._select_optimal_method(cycle_lengths)
        
        # Generate predictions using selected method
        if method == "ensemble":
            prediction_result = self._ensemble_prediction(cycle_lengths, cycle_data)
        elif method == "enhanced":
            prediction_result = self._enhanced_prediction(cycle_lengths, cycle_data)
        else:
            prediction_result = self._basic_prediction(cycle_lengths)
        
        # Add feature engineering insights
        feature_insights = self._generate_feature_insights(cycle_lengths, cycle_data)
        
        # Calculate adaptive confidence
        adaptive_confidence = self._calculate_adaptive_confidence(
            cycle_lengths, prediction_result, cycle_data
        )
        
        # Generate comprehensive recommendations
        recommendations = self._generate_comprehensive_recommendations(
            prediction_result, adaptive_confidence, feature_insights
        )
        
        # Create final result
        final_result = {
            "method": method,
            "predictions": prediction_result,
            "feature_insights": feature_insights,
            "adaptive_confidence": adaptive_confidence,
            "recommendations": recommendations,
            "accuracy_metrics": self._calculate_accuracy_metrics(prediction_result, adaptive_confidence),
            "next_steps": self._suggest_next_steps(cycle_lengths, adaptive_confidence),
            "prediction_metadata": {
                "data_points": len(cycle_lengths),
                "prediction_date": datetime.now().isoformat(),
                "algorithm_version": "2.0",
                "features_used": len(feature_insights.get("available_features", [])),
                "confidence_tier": adaptive_confidence.get("confidence_tier", "unknown")
            }
        }
        
        return final_result
    
    def _select_optimal_method(self, cycle_lengths: List[int]) -> str:
        """Select the optimal prediction method based on data characteristics."""
        n_cycles = len(cycle_lengths)
        
        # Check data quality
        if n_cycles >= self.method_thresholds["ensemble"]:
            # Check if data quality supports ensemble
            std_dev = np.std(cycle_lengths) if n_cycles > 1 else 0
            if std_dev < 20:  # Not too variable
                return "ensemble"
        
        if n_cycles >= self.method_thresholds["enhanced"]:
            return "enhanced"
        
        if n_cycles >= self.method_thresholds["basic"]:
            return "basic"
        
        return "insufficient"
    
    def _ensemble_prediction(self, cycle_lengths: List[int], 
                           cycle_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate ensemble predictions."""
        try:
            return self.ensemble_predictor.predict_ensemble(cycle_lengths)
        except Exception as e:
            # Fallback to enhanced if ensemble fails
            print(f"Ensemble prediction failed: {e}. Falling back to enhanced method.")
            return self._enhanced_prediction(cycle_lengths, cycle_data)
    
    def _enhanced_prediction(self, cycle_lengths: List[int],
                           cycle_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate enhanced predictions."""
        try:
            return self.enhanced_predictor.predict_with_insights(cycle_lengths)
        except Exception as e:
            # Fallback to basic if enhanced fails
            print(f"Enhanced prediction failed: {e}. Falling back to basic method.")
            return self._basic_prediction(cycle_lengths)
    
    def _basic_prediction(self, cycle_lengths: List[int]) -> Dict[str, Any]:
        """Generate basic predictions."""
        return predict_next_cycles(cycle_lengths)
    
    def _generate_feature_insights(self, cycle_lengths: List[int],
                                 cycle_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate comprehensive feature insights."""
        insights = {}
        
        # Basic feature summary
        basic_summary = self.feature_engineer.generate_feature_summary(cycle_lengths, cycle_data)
        insights.update(basic_summary)
        
        # Extract features if possible
        if len(cycle_lengths) >= 2:
            basic_features = self.feature_engineer.extract_features(cycle_lengths)
            insights["available_features"] = self.feature_engineer.feature_names
            
            # Feature importance (using correlation with targets)
            if len(basic_features) > 0:
                # Use cycle changes as pseudo-targets for importance analysis
                if len(cycle_lengths) > 1:
                    targets = np.diff(cycle_lengths)
                    if len(targets) == len(basic_features):
                        importance = self.feature_engineer.analyze_feature_importance(basic_features, targets)
                        insights["feature_importance"] = importance
        
        # Lifestyle features if available
        if cycle_data:
            lifestyle_features = self.feature_engineer.extract_lifestyle_features(cycle_data)
            if len(lifestyle_features) > 0:
                insights["lifestyle_features_available"] = True
                insights["lifestyle_feature_count"] = lifestyle_features.shape[1]
                
                # Analyze lifestyle patterns
                insights["lifestyle_patterns"] = self._analyze_lifestyle_patterns(cycle_data)
        
        return insights
    
    def _analyze_lifestyle_patterns(self, cycle_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze lifestyle patterns from cycle data."""
        patterns = {}
        
        # Sleep patterns
        sleep_values = [c.get("sleep_hours") for c in cycle_data if c.get("sleep_hours") is not None]
        if sleep_values:
            patterns["sleep"] = {
                "average": round(np.mean(sleep_values), 1),
                "consistency": round(1.0 - (np.std(sleep_values) / np.mean(sleep_values)), 2),
                "trend": "improving" if len(sleep_values) >= 3 and sleep_values[-1] > sleep_values[0] else "stable"
            }
        
        # Stress patterns
        stress_values = [c.get("stress") for c in cycle_data if c.get("stress") is not None]
        if stress_values:
            patterns["stress"] = {
                "average": round(np.mean(stress_values), 1),
                "consistency": round(1.0 - (np.std(stress_values) / 10), 2),
                "trend": "improving" if len(stress_values) >= 3 and stress_values[-1] < stress_values[0] else "stable"
            }
        
        # Exercise patterns
        exercise_values = [c.get("exercise", "").lower() for c in cycle_data if c.get("exercise")]
        if exercise_values:
            exercise_counts = {"none": 0, "light": 0, "moderate": 0, "heavy": 0}
            for ex in exercise_values:
                if ex in exercise_counts:
                    exercise_counts[ex] += 1
            patterns["exercise"] = exercise_counts
        
        return patterns
    
    def _calculate_adaptive_confidence(self, cycle_lengths: List[int],
                                     prediction_result: Dict[str, Any],
                                     cycle_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Calculate adaptive confidence with all available data."""
        
        # Extract predictions
        predictions = prediction_result.get("next_cycles", [])
        
        # Prepare historical data if available
        historical_data = None
        if cycle_data and len(cycle_data) > 1:
            # This would need actual historical predictions vs actuals
            # For now, we'll use a placeholder
            historical_data = {
                "past_predictions": [c.get("predicted_length", c.get("cycle_length", 28)) for c in cycle_data[-3:]],
                "actual_values": [c.get("cycle_length", 28) for c in cycle_data[-3:]]
            }
        
        # Prepare lifestyle factors
        lifestyle_factors = None
        if cycle_data:
            lifestyle_factors = {
                "stress_consistency": self._calculate_consistency(cycle_data, "stress"),
                "sleep_regularity": self._calculate_consistency(cycle_data, "sleep_hours"),
                "exercise_consistency": self._calculate_consistency(cycle_data, "exercise"),
                "symptom_completeness": self._calculate_symptom_completeness(cycle_data)
            }
        
        return self.confidence_scorer.calculate_adaptive_confidence(
            cycle_lengths, predictions, historical_data, lifestyle_factors
        )
    
    def _calculate_consistency(self, cycle_data: List[Dict[str, Any]], field: str) -> float:
        """Calculate consistency score for a lifestyle factor."""
        values = [c.get(field) for c in cycle_data if c.get(field) is not None]
        if not values:
            return 0.5
        
        if field == "exercise":
            # For exercise, check if there's a consistent pattern
            exercise_types = list(set(values))
            return max(0.2, 1.0 - (len(exercise_types) - 1) * 0.2)
        else:
            # For numeric values, use inverse of coefficient of variation
            if len(values) > 1:
                mean_val = np.mean(values)
                if mean_val > 0:
                    cv = np.std(values) / mean_val
                    return max(0.1, 1.0 - cv)
            return 0.5
    
    def _calculate_symptom_completeness(self, cycle_data: List[Dict[str, Any]]) -> float:
        """Calculate symptom tracking completeness."""
        symptom_counts = [len(c.get("symptoms", [])) for c in cycle_data]
        if not symptom_counts:
            return 0.5
        
        # Higher completeness for consistent symptom tracking
        non_zero_counts = [count for count in symptom_counts if count > 0]
        if len(non_zero_counts) == 0:
            return 0.3  # No symptom tracking
        
        completeness_ratio = len(non_zero_counts) / len(symptom_counts)
        return completeness_ratio
    
    def _generate_comprehensive_recommendations(self, prediction_result: Dict[str, Any],
                                             adaptive_confidence: Dict[str, Any],
                                             feature_insights: Dict[str, Any]) -> List[str]:
        """Generate comprehensive recommendations based on all analysis."""
        recommendations = []
        
        # Confidence-based recommendations
        confidence = adaptive_confidence.get("overall_confidence", 0)
        if confidence < 0.4:
            recommendations.append("Focus on consistent tracking to improve prediction accuracy.")
        elif confidence < 0.6:
            recommendations.append("Continue regular tracking for more reliable predictions.")
        elif confidence >= 0.8:
            recommendations.append("Excellent prediction accuracy! Maintain your tracking routine.")
        
        # Pattern-based recommendations
        if "pattern_analysis" in prediction_result:
            patterns = prediction_result["pattern_analysis"].get("detected_patterns", [])
            if "irregular" in patterns:
                recommendations.append("Consider tracking additional factors to understand cycle variability.")
            elif "regular" in patterns:
                recommendations.append("Your regular cycles make predictions highly reliable!")
        
        # Feature-based recommendations
        if "feature_importance" in feature_insights:
            importance = feature_insights["feature_importance"]
            if importance.get("local_volatility", 0) > 0.7:
                recommendations.append("High volatility detected - stress management may help regularize cycles.")
        
        # Lifestyle-based recommendations
        if "lifestyle_patterns" in feature_insights:
            lifestyle = feature_insights["lifestyle_patterns"]
            if "sleep" in lifestyle and lifestyle["sleep"]["consistency"] < 0.5:
                recommendations.append("Improving sleep consistency may help with cycle regularity.")
            if "stress" in lifestyle and lifestyle["stress"]["average"] > 6:
                recommendations.append("High stress levels detected - consider stress management techniques.")
        
        # Data quantity recommendations
        data_points = len(prediction_result.get("input_cycles", []))
        if data_points < 6:
            recommendations.append(f"Track {6 - data_points} more cycles for significantly better predictions.")
        elif data_points < 12:
            recommendations.append(f"Track {12 - data_points} more cycles to enable seasonal pattern detection.")
        
        return recommendations[:4]  # Return top 4 recommendations
    
    def _calculate_accuracy_metrics(self, prediction_result: Dict[str, Any],
                                  adaptive_confidence: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive accuracy metrics."""
        metrics = {}
        
        # Basic confidence metrics
        metrics["confidence_score"] = adaptive_confidence.get("overall_confidence", 0)
        metrics["confidence_tier"] = adaptive_confidence.get("confidence_tier", "unknown")
        
        # Prediction stability
        predictions = prediction_result.get("next_cycles", [])
        if predictions:
            pred_values = [p["predicted_length_days"] for p in predictions]
            metrics["prediction_variance"] = round(np.var(pred_values), 2)
            metrics["prediction_range"] = round(max(pred_values) - min(pred_values), 1)
            
            # Average individual confidence
            individual_confidences = [p.get("confidence", 0) for p in predictions]
            metrics["average_individual_confidence"] = round(np.mean(individual_confidences), 3)
        
        # Method-specific metrics
        method = prediction_result.get("method", "unknown")
        metrics["prediction_method"] = method
        
        if method == "ensemble":
            ensemble_data = prediction_result.get("consensus_analysis", {})
            metrics["consensus_level"] = ensemble_data.get("consensus_level", "unknown")
            metrics["agreement_score"] = ensemble_data.get("agreement_score", 0)
        
        # Estimated accuracy based on confidence tier
        confidence_tiers = {
            "excellent": 0.95,
            "good": 0.85,
            "moderate": 0.70,
            "poor": 0.50,
            "very_poor": 0.30
        }
        tier = metrics["confidence_tier"]
        metrics["estimated_accuracy"] = confidence_tiers.get(tier, 0.5)
        
        return metrics
    
    def _suggest_next_steps(self, cycle_lengths: List[int],
                          adaptive_confidence: Dict[str, Any]) -> List[str]:
        """Suggest next steps for the user."""
        steps = []
        
        confidence = adaptive_confidence.get("overall_confidence", 0)
        current_count = len(cycle_lengths)
        
        # Immediate next steps
        if current_count < 3:
            steps.append("Log your next 2-3 cycles to establish a baseline pattern.")
        elif current_count < 6:
            steps.append("Continue tracking for 2-3 more cycles to improve prediction reliability.")
        
        # Medium-term goals
        if current_count < 12:
            steps.append("Track consistently for the next few months to enable seasonal pattern analysis.")
        
        # Quality improvement
        if confidence < 0.6:
            steps.append("Focus on consistent tracking habits and complete symptom logging.")
        
        # Advanced features
        if current_count >= 6 and confidence >= 0.7:
            steps.append("Consider exploring lifestyle factors that influence your cycles.")
        
        return steps[:3]  # Return top 3 next steps
    
    def _insufficient_data_response(self) -> Dict[str, Any]:
        """Return response for insufficient data."""
        return {
            "method": "insufficient",
            "predictions": {
                "next_cycles": [],
                "overall_confidence": 0.0,
                "message": "Need at least 2 cycles for prediction. More cycles improve accuracy significantly."
            },
            "feature_insights": {"error": "Insufficient data for feature analysis"},
            "adaptive_confidence": {
                "overall_confidence": 0.1,
                "confidence_tier": "very_poor",
                "explanation": "Insufficient data for reliable predictions."
            },
            "recommendations": ["Track at least 2 more cycles to enable basic predictions"],
            "accuracy_metrics": {"estimated_accuracy": 0.1},
            "next_steps": ["Log your next cycle dates to begin tracking"]
        }


# Global improved predictor instance
improved_predictor = ImprovedPredictor()
