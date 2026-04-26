"""
Ensemble prediction system combining multiple algorithms for improved accuracy.
Uses weighted voting and confidence-based model selection.
"""
from __future__ import annotations

import numpy as np
from typing import Any, Dict, List, Tuple
from scipy import stats
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from app.services.ml_predictor import predict_next_cycles, _load_keras_model


class EnsemblePredictor:
    """Advanced ensemble predictor with multiple algorithms."""
    
    def __init__(self):
        self.algorithms = {
            "lstm": self._lstm_predict,
            "moving_average": self._moving_average_predict,
            "linear_regression": self._linear_regression_predict,
            "random_forest": self._random_forest_predict,
            "exponential_smoothing": self._exponential_smoothing_predict,
            "seasonal_decompose": self._seasonal_decompose_predict
        }
        self.weights = {
            "lstm": 0.3,
            "moving_average": 0.15,
            "linear_regression": 0.2,
            "random_forest": 0.15,
            "exponential_smoothing": 0.1,
            "seasonal_decompose": 0.1
        }
    
    def predict_ensemble(self, cycle_lengths: List[int]) -> Dict[str, Any]:
        """Generate ensemble prediction with confidence scoring."""
        if len(cycle_lengths) < 2:
            return self._insufficient_data_response()
        
        # Get predictions from all algorithms
        predictions = {}
        confidences = {}
        
        for alg_name, alg_func in self.algorithms.items():
            try:
                pred, conf = alg_func(cycle_lengths)
                predictions[alg_name] = pred
                confidences[alg_name] = conf
            except Exception as e:
                # Fallback to moving average if algorithm fails
                pred, conf = self._moving_average_predict(cycle_lengths)
                predictions[alg_name] = pred
                confidences[alg_name] = conf * 0.5  # Penalize failed algorithms
        
        # Calculate ensemble prediction using weighted average
        ensemble_prediction = self._weighted_ensemble(predictions, confidences)
        
        # Calculate ensemble confidence
        ensemble_confidence = self._calculate_ensemble_confidence(confidences, predictions)
        
        # Detect consensus and outliers
        consensus_analysis = self._analyze_consensus(predictions)
        
        # Adaptive weight adjustment based on performance
        adaptive_weights = self._adjust_weights(confidences, cycle_lengths)
        
        return {
            "method": "ensemble",
            "next_cycles": ensemble_prediction,
            "overall_confidence": ensemble_confidence,
            "individual_predictions": predictions,
            "individual_confidences": confidences,
            "consensus_analysis": consensus_analysis,
            "adaptive_weights": adaptive_weights,
            "ensemble_size": len([p for p in predictions.values() if p]),
            "recommendation": self._generate_ensemble_recommendation(ensemble_confidence, consensus_analysis)
        }
    
    def _lstm_predict(self, cycle_lengths: List[int]) -> Tuple[List[Dict[str, Any]], float]:
        """LSTM prediction from existing model."""
        result = predict_next_cycles(cycle_lengths)
        if result["method"] == "lstm":
            return result["next_cycles"], result.get("overall_confidence", 0.5)
        else:
            # LSTM not available, return low confidence
            return [], 0.1
    
    def _moving_average_predict(self, cycle_lengths: List[int]) -> Tuple[List[Dict[str, Any]], float]:
        """Enhanced moving average with trend adjustment."""
        if len(cycle_lengths) < 2:
            return [], 0.0
        
        # Calculate different window sizes
        recent = cycle_lengths[-3:] if len(cycle_lengths) >= 3 else cycle_lengths
        longer = cycle_lengths[-6:] if len(cycle_lengths) >= 6 else cycle_lengths
        
        recent_avg = np.mean(recent)
        longer_avg = np.mean(longer)
        
        # Detect trend
        if len(cycle_lengths) >= 4:
            trend_slope = np.polyfit(range(len(cycle_lengths[-4:])), cycle_lengths[-4:], 1)[0]
            trend_adjustment = trend_slope * 2  # Apply trend to future predictions
        else:
            trend_adjustment = 0
        
        # Generate predictions
        predictions = []
        base_value = cycle_lengths[-1]
        
        for i in range(1, 4):
            # Weighted combination of recent and longer averages with trend
            pred_value = 0.6 * recent_avg + 0.4 * longer_avg + trend_adjustment * i
            
            # Add some variance based on historical volatility
            std_dev = np.std(cycle_lengths)
            variance_factor = min(0.1, std_dev / 50)
            noise = np.random.normal(0, variance_factor * pred_value)
            
            pred_value = max(15, min(90, pred_value + noise))
            
            confidence = max(0.2, 1.0 - (std_dev / 30))
            
            predictions.append({
                "cycle_index": i,
                "predicted_length_days": round(pred_value, 1),
                "interval_low": round(max(15, pred_value - std_dev), 1),
                "interval_high": round(min(90, pred_value + std_dev), 1),
                "confidence": round(confidence, 2)
            })
        
        avg_confidence = np.mean([p["confidence"] for p in predictions])
        return predictions, avg_confidence
    
    def _linear_regression_predict(self, cycle_lengths: List[int]) -> Tuple[List[Dict[str, Any]], float]:
        """Linear regression with polynomial features."""
        if len(cycle_lengths) < 3:
            return [], 0.0
        
        X = np.array(range(len(cycle_lengths))).reshape(-1, 1)
        y = np.array(cycle_lengths)
        
        # Try polynomial regression
        try:
            # Fit polynomial of degree 2
            coeffs = np.polyfit(X.flatten(), y, 2)
            
            # Predict next 3 cycles
            predictions = []
            for i in range(1, 4):
                next_x = len(cycle_lengths) + i
                pred_value = coeffs[0] * next_x**2 + coeffs[1] * next_x + coeffs[2]
                pred_value = max(15, min(90, pred_value))
                
                # Calculate confidence based on fit quality
                y_pred = np.polyval(coeffs, X.flatten())
                mse = np.mean((y - y_pred) ** 2)
                confidence = max(0.2, 1.0 - (mse / 100))
                
                predictions.append({
                    "cycle_index": i,
                    "predicted_length_days": round(pred_value, 1),
                    "interval_low": round(max(15, pred_value - np.sqrt(mse)), 1),
                    "interval_high": round(min(90, pred_value + np.sqrt(mse)), 1),
                    "confidence": round(confidence, 2)
                })
            
            avg_confidence = np.mean([p["confidence"] for p in predictions])
            return predictions, avg_confidence
            
        except:
            return self._moving_average_predict(cycle_lengths)
    
    def _random_forest_predict(self, cycle_lengths: List[int]) -> Tuple[List[Dict[str, Any]], float]:
        """Random Forest regression for non-linear patterns."""
        if len(cycle_lengths) < 4:
            return [], 0.0
        
        try:
            # Prepare features
            X = []
            y = []
            
            for i in range(2, len(cycle_lengths)):
                # Use last 2 cycles as features
                features = [
                    cycle_lengths[i-2],
                    cycle_lengths[i-1],
                    i,  # position
                    np.mean(cycle_lengths[:i]),  # running average
                    np.std(cycle_lengths[:i]) if i > 1 else 0  # running std
                ]
                X.append(features)
                y.append(cycle_lengths[i])
            
            # Train Random Forest
            rf = RandomForestRegressor(n_estimators=50, random_state=42)
            rf.fit(X, y)
            
            # Predict next 3 cycles
            predictions = []
            for i in range(1, 4):
                features = [
                    cycle_lengths[-2] if len(cycle_lengths) >= 2 else cycle_lengths[-1],
                    cycle_lengths[-1],
                    len(cycle_lengths) + i,
                    np.mean(cycle_lengths),
                    np.std(cycle_lengths) if len(cycle_lengths) > 1 else 0
                ]
                
                pred_value = rf.predict([features])[0]
                pred_value = max(15, min(90, pred_value))
                
                # Calculate confidence based on prediction variance
                tree_predictions = [tree.predict([features])[0] for tree in rf.estimators_]
                pred_std = np.std(tree_predictions)
                confidence = max(0.2, 1.0 - (pred_std / 20))
                
                predictions.append({
                    "cycle_index": i,
                    "predicted_length_days": round(pred_value, 1),
                    "interval_low": round(max(15, pred_value - pred_std), 1),
                    "interval_high": round(min(90, pred_value + pred_std), 1),
                    "confidence": round(confidence, 2)
                })
            
            avg_confidence = np.mean([p["confidence"] for p in predictions])
            return predictions, avg_confidence
            
        except:
            return self._moving_average_predict(cycle_lengths)
    
    def _exponential_smoothing_predict(self, cycle_lengths: List[int]) -> Tuple[List[Dict[str, Any]], float]:
        """Exponential smoothing for trend-aware predictions."""
        if len(cycle_lengths) < 2:
            return [], 0.0
        
        # Calculate optimal alpha using simple optimization
        def exponential_smooth(data, alpha):
            smoothed = [data[0]]
            for i in range(1, len(data)):
                smoothed.append(alpha * data[i] + (1 - alpha) * smoothed[-1])
            return smoothed
        
        best_alpha = 0.3
        best_mse = float('inf')
        
        for alpha in [0.1, 0.2, 0.3, 0.4, 0.5]:
            smoothed = exponential_smooth(cycle_lengths, alpha)
            mse = np.mean((cycle_lengths[1:] - smoothed[:-1]) ** 2)
            if mse < best_mse:
                best_mse = mse
                best_alpha = alpha
        
        # Generate predictions
        smoothed = exponential_smooth(cycle_lengths, best_alpha)
        last_smoothed = smoothed[-1]
        
        # Calculate trend
        if len(smoothed) >= 2:
            trend = smoothed[-1] - smoothed[-2]
        else:
            trend = 0
        
        predictions = []
        for i in range(1, 4):
            pred_value = last_smoothed + trend * i
            pred_value = max(15, min(90, pred_value))
            
            confidence = max(0.2, 1.0 - (best_mse / 50))
            
            predictions.append({
                "cycle_index": i,
                "predicted_length_days": round(pred_value, 1),
                "interval_low": round(max(15, pred_value - np.sqrt(best_mse)), 1),
                "interval_high": round(min(90, pred_value + np.sqrt(best_mse)), 1),
                "confidence": round(confidence, 2)
            })
        
        avg_confidence = np.mean([p["confidence"] for p in predictions])
        return predictions, avg_confidence
    
    def _seasonal_decompose_predict(self, cycle_lengths: List[int]) -> Tuple[List[Dict[str, Any]], float]:
        """Simple seasonal decomposition for patterns."""
        if len(cycle_lengths) < 12:
            return [], 0.0
        
        try:
            # Simple seasonal pattern detection
            # Assume 12-cycle seasonality (yearly pattern)
            seasonal_period = 12
            
            if len(cycle_lengths) >= seasonal_period + 3:
                # Calculate seasonal pattern
                seasonal_pattern = []
                for i in range(seasonal_period):
                    seasonal_values = [cycle_lengths[j] for j in range(i, len(cycle_lengths), seasonal_period)]
                    seasonal_pattern.append(np.mean(seasonal_values))
                
                # Calculate trend
                trend_slope = np.polyfit(range(len(cycle_lengths)), cycle_lengths, 1)[0]
                
                predictions = []
                for i in range(1, 4):
                    future_pos = len(cycle_lengths) + i
                    seasonal_idx = (future_pos - 1) % seasonal_period
                    
                    # Combine trend and seasonal
                    pred_value = cycle_lengths[-1] + trend_slope * i + (seasonal_pattern[seasonal_idx] - np.mean(seasonal_pattern))
                    pred_value = max(15, min(90, pred_value))
                    
                    # Calculate confidence
                    seasonal_var = np.var(seasonal_pattern)
                    confidence = max(0.2, 1.0 - (seasonal_var / 100))
                    
                    predictions.append({
                        "cycle_index": i,
                        "predicted_length_days": round(pred_value, 1),
                        "interval_low": round(max(15, pred_value - np.sqrt(seasonal_var)), 1),
                        "interval_high": round(min(90, pred_value + np.sqrt(seasonal_var)), 1),
                        "confidence": round(confidence, 2)
                    })
                
                avg_confidence = np.mean([p["confidence"] for p in predictions])
                return predictions, avg_confidence
            else:
                return [], 0.0
                
        except:
            return [], 0.0
    
    def _weighted_ensemble(self, predictions: Dict[str, List[Dict[str, Any]]], 
                          confidences: Dict[str, float]) -> List[Dict[str, Any]]:
        """Calculate weighted ensemble prediction."""
        if not predictions:
            return []
        
        # Get the first prediction structure to follow the format
        first_valid_pred = None
        for pred in predictions.values():
            if pred:
                first_valid_pred = pred
                break
        
        if not first_valid_pred:
            return []
        
        ensemble_predictions = []
        
        for i in range(len(first_valid_pred)):
            # Collect predictions for cycle i+1 from all algorithms
            cycle_predictions = []
            cycle_weights = []
            
            for alg_name, alg_preds in predictions.items():
                if alg_preds and i < len(alg_preds):
                    cycle_predictions.append(alg_preds[i]["predicted_length_days"])
                    # Use confidence as weight
                    weight = confidences.get(alg_name, 0.1) * self.weights.get(alg_name, 0.1)
                    cycle_weights.append(weight)
            
            if cycle_predictions:
                # Calculate weighted average
                total_weight = sum(cycle_weights)
                if total_weight > 0:
                    weighted_pred = sum(p * w for p, w in zip(cycle_predictions, cycle_weights)) / total_weight
                else:
                    weighted_pred = np.mean(cycle_predictions)
                
                # Calculate ensemble confidence for this cycle
                ensemble_conf = sum(cycle_weights) / sum(self.weights.values())
                ensemble_conf = min(0.95, ensemble_conf)  # Cap confidence
                
                # Calculate prediction variance for interval
                pred_variance = np.var(cycle_predictions) if len(cycle_predictions) > 1 else 4
                
                ensemble_predictions.append({
                    "cycle_index": i + 1,
                    "predicted_length_days": round(weighted_pred, 1),
                    "interval_low": round(max(15, weighted_pred - np.sqrt(pred_variance)), 1),
                    "interval_high": round(min(90, weighted_pred + np.sqrt(pred_variance)), 1),
                    "confidence": round(ensemble_conf, 2)
                })
        
        return ensemble_predictions
    
    def _calculate_ensemble_confidence(self, confidences: Dict[str, float], 
                                     predictions: Dict[str, List[Dict[str, Any]]]) -> float:
        """Calculate overall ensemble confidence."""
        if not confidences:
            return 0.0
        
        # Weighted confidence based on algorithm weights
        weighted_confidence = 0.0
        total_weight = 0.0
        
        for alg_name, conf in confidences.items():
            weight = self.weights.get(alg_name, 0.1)
            weighted_confidence += conf * weight
            total_weight += weight
        
        base_confidence = weighted_confidence / total_weight if total_weight > 0 else 0.0
        
        # Boost confidence if algorithms agree
        if len(predictions) > 1:
            # Calculate prediction variance across algorithms
            all_predictions = []
            for alg_preds in predictions.values():
                if alg_preds:
                    all_predictions.append(alg_preds[0]["predicted_length_days"])
            
            if len(all_predictions) > 1:
                pred_variance = np.var(all_predictions)
                agreement_bonus = max(0, 1.0 - (pred_variance / 50))
                base_confidence = min(0.95, base_confidence + agreement_bonus * 0.1)
        
        return round(base_confidence, 2)
    
    def _analyze_consensus(self, predictions: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Analyze consensus and outliers among algorithms."""
        if len(predictions) < 2:
            return {"consensus_level": "insufficient_data"}
        
        # Get first cycle predictions from all algorithms
        first_cycle_preds = []
        for alg_preds in predictions.values():
            if alg_preds:
                first_cycle_preds.append(alg_preds[0]["predicted_length_days"])
        
        if len(first_cycle_preds) < 2:
            return {"consensus_level": "insufficient_data"}
        
        # Calculate consensus metrics
        mean_pred = np.mean(first_cycle_preds)
        std_pred = np.std(first_cycle_preds)
        
        # Determine consensus level
        if std_pred < 2:
            consensus_level = "high"
        elif std_pred < 5:
            consensus_level = "medium"
        else:
            consensus_level = "low"
        
        # Identify outliers
        outliers = []
        for i, pred in enumerate(first_cycle_preds):
            if abs(pred - mean_pred) > 2 * std_pred:
                outliers.append({
                    "algorithm": list(predictions.keys())[i],
                    "prediction": pred,
                    "deviation": abs(pred - mean_pred)
                })
        
        return {
            "consensus_level": consensus_level,
            "mean_prediction": round(mean_pred, 1),
            "std_deviation": round(std_pred, 1),
            "outliers": outliers,
            "agreement_score": round(max(0, 1.0 - (std_pred / 20)), 2)
        }
    
    def _adjust_weights(self, confidences: Dict[str, float], cycle_lengths: List[int]) -> Dict[str, float]:
        """Adaptively adjust weights based on recent performance."""
        adjusted_weights = {}
        
        # Base adjustment on data characteristics
        data_volatility = np.std(cycle_lengths) if len(cycle_lengths) > 1 else 0
        data_length = len(cycle_lengths)
        
        for alg_name, base_weight in self.weights.items():
            conf = confidences.get(alg_name, 0.1)
            
            # Adjust weight based on confidence
            adjusted_weight = base_weight * (0.5 + conf)
            
            # Special adjustments for specific algorithms
            if alg_name == "lstm" and data_length < 6:
                adjusted_weight *= 0.5  # Penalize LSTM with limited data
            elif alg_name == "seasonal_decompose" and data_length < 12:
                adjusted_weight *= 0.1  # Heavily penalize seasonal with insufficient data
            elif alg_name == "random_forest" and data_volatility < 3:
                adjusted_weight *= 0.8  # Slightly penalize RF for very regular data
            elif alg_name == "moving_average" and data_volatility > 8:
                adjusted_weight *= 0.7  # Penalize MA for highly variable data
            
            adjusted_weights[alg_name] = adjusted_weight
        
        # Normalize weights
        total_weight = sum(adjusted_weights.values())
        if total_weight > 0:
            adjusted_weights = {k: v / total_weight for k, v in adjusted_weights.items()}
        
        return adjusted_weights
    
    def _generate_ensemble_recommendation(self, confidence: float, consensus: Dict[str, Any]) -> str:
        """Generate recommendation based on ensemble results."""
        if confidence >= 0.8:
            return "High confidence ensemble prediction. Multiple algorithms agree strongly."
        elif confidence >= 0.6:
            consensus_level = consensus.get("consensus_level", "unknown")
            if consensus_level == "high":
                return "Good confidence with strong algorithm consensus."
            else:
                return "Moderate confidence. Algorithms show some disagreement - continue tracking."
        else:
            return "Lower confidence due to limited data or high variability. More cycles will improve accuracy."
    
    def _insufficient_data_response(self) -> Dict[str, Any]:
        """Return response for insufficient data."""
        return {
            "method": "ensemble",
            "next_cycles": [],
            "overall_confidence": 0.0,
            "message": "Need at least 2 cycles for ensemble prediction. More cycles improve accuracy significantly.",
            "recommendation": "Continue tracking to enable advanced ensemble predictions."
        }


# Global ensemble predictor instance
ensemble_predictor = EnsemblePredictor()
