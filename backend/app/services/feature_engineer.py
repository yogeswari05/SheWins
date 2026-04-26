"""
Feature engineering service for enhanced prediction accuracy.
Extracts meaningful features from raw cycle data.
"""
from __future__ import annotations

import numpy as np
from typing import Any, Dict, List, Optional, Tuple
from scipy import stats
from datetime import datetime, timedelta
import statistics


class FeatureEngineer:
    """Advanced feature engineering for cycle prediction."""
    
    def __init__(self):
        self.feature_names = [
            "cycle_length", "cycle_change", "local_trend", "local_volatility",
            "cycle_position", "seasonal_component", "outlier_score",
            "momentum", "acceleration", "regression_score", "forecast_error"
        ]
    
    def extract_features(self, cycle_lengths: List[int], cycle_data: Optional[List[Dict[str, Any]]] = None) -> np.ndarray:
        """Extract comprehensive features from cycle data."""
        if len(cycle_lengths) < 2:
            return np.array([])
        
        features = []
        
        for i in range(len(cycle_lengths)):
            cycle_features = []
            
            # Basic features
            cycle_features.append(cycle_lengths[i] / 35.0)  # normalized cycle length
            
            # Cycle change from previous
            if i > 0:
                cycle_change = (cycle_lengths[i] - cycle_lengths[i-1]) / cycle_lengths[i-1]
                cycle_features.append(cycle_change)
            else:
                cycle_features.append(0.0)
            
            # Local trend (last 3 cycles)
            if i >= 2:
                recent_cycles = cycle_lengths[max(0, i-2):i+1]
                trend_slope = np.polyfit(range(len(recent_cycles)), recent_cycles, 1)[0]
                cycle_features.append(trend_slope / 5.0)  # normalized trend
            else:
                cycle_features.append(0.0)
            
            # Local volatility
            if i >= 2:
                recent_cycles = cycle_lengths[max(0, i-2):i+1]
                volatility = np.std(recent_cycles)
                cycle_features.append(volatility / 10.0)  # normalized volatility
            else:
                cycle_features.append(0.1)
            
            # Cycle position (relative to average)
            if i > 0:
                avg_so_far = np.mean(cycle_lengths[:i])
                position = (cycle_lengths[i] - avg_so_far) / avg_so_far
                cycle_features.append(position)
            else:
                cycle_features.append(0.0)
            
            # Seasonal component (if enough data)
            if len(cycle_lengths) >= 12:
                seasonal_idx = i % 12
                seasonal_avg = np.mean([cycle_lengths[j] for j in range(seasonal_idx, len(cycle_lengths), 12)])
                overall_avg = np.mean(cycle_lengths)
                seasonal_component = (seasonal_avg - overall_avg) / overall_avg
                cycle_features.append(seasonal_component)
            else:
                cycle_features.append(0.0)
            
            # Outlier score
            if i >= 3:
                recent_avg = np.mean(cycle_lengths[max(0, i-3):i])
                recent_std = np.std(cycle_lengths[max(0, i-3):i])
                if recent_std > 0:
                    outlier_score = abs(cycle_lengths[i] - recent_avg) / recent_std
                else:
                    outlier_score = 0.0
                cycle_features.append(min(3.0, outlier_score) / 3.0)  # capped and normalized
            else:
                cycle_features.append(0.0)
            
            # Momentum (rate of change)
            if i >= 1:
                momentum = (cycle_lengths[i] - cycle_lengths[i-1]) / cycle_lengths[i-1]
                cycle_features.append(np.tanh(momentum))  # bounded between -1 and 1
            else:
                cycle_features.append(0.0)
            
            # Acceleration (change in momentum)
            if i >= 2:
                mom1 = (cycle_lengths[i] - cycle_lengths[i-1]) / cycle_lengths[i-1]
                mom2 = (cycle_lengths[i-1] - cycle_lengths[i-2]) / cycle_lengths[i-2]
                acceleration = mom1 - mom2
                cycle_features.append(np.tanh(acceleration))
            else:
                cycle_features.append(0.0)
            
            # Regression score (how well recent data fits a linear trend)
            if i >= 3:
                recent_cycles = cycle_lengths[max(0, i-3):i+1]
                x = np.arange(len(recent_cycles))
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, recent_cycles)
                cycle_features.append(max(0, r_value ** 2))  # R-squared
            else:
                cycle_features.append(0.5)
            
            # Forecast error (how well simple predictions would have worked)
            if i >= 2:
                # Simple moving average prediction
                ma_pred = np.mean(cycle_lengths[max(0, i-2):i])
                forecast_error = abs(cycle_lengths[i] - ma_pred) / ma_pred
                cycle_features.append(min(2.0, forecast_error) / 2.0)  # capped and normalized
            else:
                cycle_features.append(0.0)
            
            features.append(cycle_features)
        
        return np.array(features, dtype=np.float32)
    
    def extract_lifestyle_features(self, cycle_data: List[Dict[str, Any]]) -> np.ndarray:
        """Extract lifestyle features from cycle data."""
        if not cycle_data:
            return np.array([])
        
        features = []
        
        for cycle in cycle_data:
            cycle_features = []
            
            # Sleep features
            sleep_hours = cycle.get("sleep_hours")
            if sleep_hours is not None:
                cycle_features.append(sleep_hours / 10.0)  # normalized
                # Sleep quality indicators
                if sleep_hours < 6:
                    cycle_features.append(1.0)  # poor sleep
                elif sleep_hours > 9:
                    cycle_features.append(0.5)  # excessive sleep
                else:
                    cycle_features.append(0.0)  # good sleep
            else:
                cycle_features.extend([0.7, 0.3])  # default values
            
            # Stress features
            stress = cycle.get("stress")
            if stress is not None:
                cycle_features.append(stress / 10.0)  # normalized
            else:
                cycle_features.append(0.5)  # default
            
            # Exercise features
            exercise = cycle.get("exercise", "").lower()
            exercise_map = {"none": 0.0, "light": 0.33, "moderate": 0.67, "heavy": 1.0}
            cycle_features.append(exercise_map.get(exercise, 0.33))
            
            # Mood features
            mood = cycle.get("mood", "").lower()
            mood_map = {
                "happy": 0.1, "calm": 0.2, "energetic": 0.3,
                "tired": 0.6, "anxious": 0.7, "irritable": 0.8,
                "sad": 0.7, "confused": 0.6, "unwell": 0.9
            }
            cycle_features.append(mood_map.get(mood, 0.5))
            
            # Symptom features
            symptoms = cycle.get("symptoms", [])
            if symptoms:
                # Symptom count
                cycle_features.append(min(1.0, len(symptoms) / 10.0))
                
                # Stress-related symptoms
                stress_symptoms = ["headache", "migraine", "fatigue", "muscle_tension"]
                stress_symptom_count = sum(1 for s in symptoms if s.lower() in stress_symptoms)
                cycle_features.append(min(1.0, stress_symptom_count / 3.0))
                
                # Hormonal symptoms
                hormonal_symptoms = ["acne", "hairfall", "weight gain", "bloating"]
                hormonal_symptom_count = sum(1 for s in symptoms if s.lower() in hormonal_symptoms)
                cycle_features.append(min(1.0, hormonal_symptom_count / 3.0))
            else:
                cycle_features.extend([0.0, 0.0, 0.0])
            
            # Flow intensity
            flow = cycle.get("flow", "").lower()
            flow_map = {"light": 0.25, "medium": 0.5, "heavy": 0.75, "spotting": 0.1}
            cycle_features.append(flow_map.get(flow, 0.5))
            
            features.append(cycle_features)
        
        return np.array(features, dtype=np.float32)
    
    def create_sequences(self, features: np.ndarray, seq_len: int = 6) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for time series models."""
        if len(features) < seq_len + 1:
            return np.array([]), np.array([])
        
        X = []
        y = []
        
        for i in range(len(features) - seq_len):
            X.append(features[i:i+seq_len])
            y.append(features[i+seq_len])  # Next cycle features
        
        return np.array(X), np.array(y)
    
    def analyze_feature_importance(self, features: np.ndarray, targets: np.ndarray) -> Dict[str, float]:
        """Analyze feature importance using correlation."""
        if features.shape[0] == 0 or targets.shape[0] == 0:
            return {}
        
        importance = {}
        for i, feature_name in enumerate(self.feature_names):
            if i < features.shape[1]:
                correlation = np.corrcoef(features[:, i], targets)[0, 1]
                importance[feature_name] = abs(correlation) if not np.isnan(correlation) else 0.0
        
        return importance
    
    def detect_anomalies(self, features: np.ndarray) -> List[int]:
        """Detect anomalous cycles based on features."""
        if len(features) == 0:
            return []
        
        anomalies = []
        
        # Z-score based anomaly detection
        for i in range(len(features)):
            z_scores = []
            for j in range(features.shape[1]):
                if len(features) > 1:
                    mean_val = np.mean(features[:, j])
                    std_val = np.std(features[:, j])
                    if std_val > 0:
                        z_score = abs(features[i, j] - mean_val) / std_val
                        z_scores.append(z_score)
            
            # Flag as anomaly if many features have high z-scores
            high_z_scores = [z for z in z_scores if z > 2.5]
            if len(high_z_scores) > features.shape[1] * 0.3:  # 30% of features are outliers
                anomalies.append(i)
        
        return anomalies
    
    def generate_feature_summary(self, cycle_lengths: List[int], cycle_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Generate comprehensive feature summary."""
        if len(cycle_lengths) < 2:
            return {"error": "Insufficient data for feature analysis"}
        
        # Extract basic features
        basic_features = self.extract_features(cycle_lengths)
        
        # Extract lifestyle features if available
        lifestyle_features = None
        if cycle_data:
            lifestyle_features = self.extract_lifestyle_features(cycle_data)
        
        # Calculate statistics
        summary = {
            "data_points": len(cycle_lengths),
            "feature_count": basic_features.shape[1] if len(basic_features) > 0 else 0,
            "lifestyle_feature_count": lifestyle_features.shape[1] if lifestyle_features is not None and len(lifestyle_features) > 0 else 0,
            "basic_features_available": len(basic_features) > 0,
            "lifestyle_features_available": lifestyle_features is not None and len(lifestyle_features) > 0
        }
        
        # Feature statistics
        if len(basic_features) > 0:
            summary["feature_statistics"] = {}
            for i, name in enumerate(self.feature_names):
                if i < basic_features.shape[1]:
                    feature_col = basic_features[:, i]
                    summary["feature_statistics"][name] = {
                        "mean": float(np.mean(feature_col)),
                        "std": float(np.std(feature_col)),
                        "min": float(np.min(feature_col)),
                        "max": float(np.max(feature_col))
                    }
        
        # Anomaly detection
        if len(basic_features) > 0:
            anomalies = self.detect_anomalies(basic_features)
            summary["anomalies"] = {
                "count": len(anomalies),
                "indices": anomalies,
                "percentage": round(len(anomalies) / len(cycle_lengths) * 100, 1)
            }
        
        return summary


# Global feature engineer instance
feature_engineer = FeatureEngineer()
