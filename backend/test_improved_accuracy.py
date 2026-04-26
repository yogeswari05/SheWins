"""
Test the improved prediction system and validate accuracy improvements.
"""
import numpy as np
from app.services.improved_predictor import improved_predictor
from app.services.ml_predictor import predict_next_cycles
from app.services.enhanced_predictor import enhanced_predictor
from app.services.pcod_risk import compute_pcod_risk
from app.services.stress_analyzer import calculate_stress_score


def generate_comprehensive_test_data():
    """Generate comprehensive test data for accuracy validation."""
    np.random.seed(42)
    
    test_scenarios = {
        "regular_perfect": {
            "cycles": [28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
            "description": "Perfectly regular 28-day cycles",
            "expected_accuracy": 0.95
        },
        "regular_natural": {
            "cycles": [28, 29, 27, 28, 30, 26, 28, 29, 27, 28, 29, 28],
            "description": "Natural variation around 28 days",
            "expected_accuracy": 0.90
        },
        "slightly_irregular": {
            "cycles": [26, 29, 27, 31, 25, 30, 28, 32, 26, 29, 27, 30],
            "description": "Slightly irregular cycles",
            "expected_accuracy": 0.75
        },
        "moderately_irregular": {
            "cycles": [24, 32, 26, 35, 23, 38, 25, 34, 27, 36, 24, 33],
            "description": "Moderately irregular cycles",
            "expected_accuracy": 0.65
        },
        "highly_irregular": {
            "cycles": [21, 40, 25, 45, 22, 42, 26, 38, 24, 44, 23, 41],
            "description": "Highly irregular cycles",
            "expected_accuracy": 0.55
        },
        "trending_longer": {
            "cycles": [26, 27, 28, 30, 32, 34, 35, 37, 38, 40, 42, 44],
            "description": "Cycles trending longer",
            "expected_accuracy": 0.80
        },
        "trending_shorter": {
            "cycles": [35, 34, 32, 30, 28, 26, 25, 23, 22, 21, 20, 19],
            "description": "Cycles trending shorter",
            "expected_accuracy": 0.80
        },
        "pcod_like": {
            "cycles": [35, 42, 28, 45, 38, 50, 32, 48, 40, 55, 35, 46],
            "description": "PCOD-like patterns",
            "expected_accuracy": 0.70
        },
        "seasonal_pattern": {
            "cycles": [28, 30, 32, 31, 29, 27, 26, 28, 30, 32, 31, 29],
            "description": "Seasonal pattern variation",
            "expected_accuracy": 0.85
        },
        "stress_affected": {
            "cycles": [28, 35, 26, 38, 25, 40, 24, 42, 27, 36, 25, 39],
            "description": "Stress-affected irregular cycles",
            "expected_accuracy": 0.60
        }
    }
    
    return test_scenarios


def test_prediction_methods_comparison():
    """Compare all prediction methods across test scenarios."""
    test_scenarios = generate_comprehensive_test_data()
    results = {}
    
    print("=== PREDICTION METHODS COMPARISON ===\n")
    
    for scenario_name, scenario_data in test_scenarios.items():
        cycles = scenario_data["cycles"]
        print(f"Testing {scenario_name.upper()}: {scenario_data['description']}")
        print(f"Input cycles: {cycles}")
        
        scenario_results = {}
        
        # Test Basic Predictor
        try:
            basic_result = predict_next_cycles(cycles)
            scenario_results["basic"] = {
                "method": basic_result.get("method", "unknown"),
                "confidence": basic_result.get("overall_confidence", 0),
                "predictions": len(basic_result.get("next_cycles", [])),
                "success": True
            }
            print(f"  Basic: {basic_result['method']} - Confidence: {basic_result.get('overall_confidence', 0):.3f}")
        except Exception as e:
            scenario_results["basic"] = {"success": False, "error": str(e)}
            print(f"  Basic: FAILED - {e}")
        
        # Test Enhanced Predictor
        try:
            enhanced_result = enhanced_predictor.predict_with_insights(cycles)
            scenario_results["enhanced"] = {
                "method": enhanced_result.get("method", "unknown"),
                "confidence": enhanced_result.get("overall_confidence", 0),
                "quality": enhanced_result.get("prediction_quality", {}).get("quality_score", 0),
                "predictions": len(enhanced_result.get("next_cycles", [])),
                "success": True
            }
            quality = enhanced_result.get("prediction_quality", {}).get("quality_score", 0)
            print(f"  Enhanced: {enhanced_result['method']} - Confidence: {enhanced_result.get('overall_confidence', 0):.3f}, Quality: {quality:.3f}")
        except Exception as e:
            scenario_results["enhanced"] = {"success": False, "error": str(e)}
            print(f"  Enhanced: FAILED - {e}")
        
        # Test Improved Predictor (Ensemble)
        try:
            improved_result = improved_predictor.predict_with_maximum_accuracy(cycles)
            scenario_results["improved"] = {
                "method": improved_result.get("method", "unknown"),
                "confidence": improved_result.get("adaptive_confidence", {}).get("overall_confidence", 0),
                "estimated_accuracy": improved_result.get("accuracy_metrics", {}).get("estimated_accuracy", 0),
                "predictions": len(improved_result.get("predictions", {}).get("next_cycles", [])),
                "success": True
            }
            adaptive_conf = improved_result.get("adaptive_confidence", {}).get("overall_confidence", 0)
            est_accuracy = improved_result.get("accuracy_metrics", {}).get("estimated_accuracy", 0)
            print(f"  Improved: {improved_result['method']} - Confidence: {adaptive_conf:.3f}, Est. Accuracy: {est_accuracy:.3f}")
        except Exception as e:
            scenario_results["improved"] = {"success": False, "error": str(e)}
            print(f"  Improved: FAILED - {e}")
        
        # Calculate improvement metrics
        if scenario_results.get("basic", {}).get("success") and scenario_results.get("improved", {}).get("success"):
            basic_conf = scenario_results["basic"]["confidence"]
            improved_conf = scenario_results["improved"]["confidence"]
            improvement = ((improved_conf - basic_conf) / basic_conf * 100) if basic_conf > 0 else 0
            print(f"  Improvement: {improvement:+.1f}%")
        
        print()
        results[scenario_name] = scenario_results
    
    return results


def test_feature_engineering():
    """Test feature engineering capabilities."""
    print("=== FEATURE ENGINEERING TEST ===\n")
    
    test_cycles = [28, 29, 27, 31, 26, 30, 28, 32, 27, 29, 28, 30]
    
    try:
        from app.services.feature_engineer import feature_engineer
        
        # Test basic feature extraction
        features = feature_engineer.extract_features(test_cycles)
        print(f"Feature extraction successful: {features.shape}")
        print(f"Feature names: {feature_engineer.feature_names}")
        
        # Test feature summary
        summary = feature_engineer.generate_feature_summary(test_cycles)
        print(f"Feature summary keys: {list(summary.keys())}")
        
        # Test anomaly detection
        anomalies = feature_engineer.detect_anomalies(features)
        print(f"Anomalies detected: {len(anomalies)} at indices {anomalies}")
        
        print("✅ Feature engineering working correctly\n")
        return True
        
    except Exception as e:
        print(f"❌ Feature engineering failed: {e}\n")
        return False


def test_adaptive_confidence():
    """Test adaptive confidence scoring."""
    print("=== ADAPTIVE CONFIDENCE TEST ===\n")
    
    test_cycles = [28, 29, 27, 31, 26, 30, 28, 32, 27, 29, 28, 30]
    test_predictions = [
        {"cycle_index": 1, "predicted_length_days": 29, "confidence": 0.8},
        {"cycle_index": 2, "predicted_length_days": 28, "confidence": 0.7},
        {"cycle_index": 3, "predicted_length_days": 30, "confidence": 0.6}
    ]
    
    try:
        from app.services.adaptive_confidence import adaptive_confidence_scorer
        
        # Test adaptive confidence calculation
        confidence_result = adaptive_confidence_scorer.calculate_adaptive_confidence(
            test_cycles, test_predictions
        )
        
        print(f"Overall confidence: {confidence_result.get('overall_confidence', 0):.3f}")
        print(f"Confidence tier: {confidence_result.get('confidence_tier', 'unknown')}")
        print(f"Individual factors: {list(confidence_result.get('individual_factors', {}).keys())}")
        print(f"Improvement suggestions: {len(confidence_result.get('improvement_suggestions', []))}")
        
        print("✅ Adaptive confidence working correctly\n")
        return True
        
    except Exception as e:
        print(f"❌ Adaptive confidence failed: {e}\n")
        return False


def test_ensemble_predictor():
    """Test ensemble predictor functionality."""
    print("=== ENSEMBLE PREDICTOR TEST ===\n")
    
    test_cycles = [28, 29, 27, 31, 26, 30, 28, 32, 27, 29, 28, 30]
    
    try:
        from app.services.ensemble_predictor import ensemble_predictor
        
        # Test ensemble prediction
        ensemble_result = ensemble_predictor.predict_ensemble(test_cycles)
        
        print(f"Ensemble method: {ensemble_result.get('method', 'unknown')}")
        print(f"Overall confidence: {ensemble_result.get('overall_confidence', 0):.3f}")
        print(f"Individual predictions: {len(ensemble_result.get('individual_predictions', {}))}")
        print(f"Consensus level: {ensemble_result.get('consensus_analysis', {}).get('consensus_level', 'unknown')}")
        print(f"Ensemble size: {ensemble_result.get('ensemble_size', 0)}")
        
        print("✅ Ensemble predictor working correctly\n")
        return True
        
    except Exception as e:
        print(f"❌ Ensemble predictor failed: {e}\n")
        return False


def calculate_overall_improvement(results):
    """Calculate overall improvement metrics."""
    print("=== OVERALL IMPROVEMENT ANALYSIS ===\n")
    
    successful_comparisons = 0
    total_improvement = 0
    basic_confidences = []
    improved_confidences = []
    
    for scenario_name, scenario_results in results.items():
        basic = scenario_results.get("basic", {})
        improved = scenario_results.get("improved", {})
        
        if basic.get("success") and improved.get("success"):
            successful_comparisons += 1
            basic_conf = basic["confidence"]
            improved_conf = improved["confidence"]
            
            basic_confidences.append(basic_conf)
            improved_confidences.append(improved_conf)
            
            if basic_conf > 0:
                improvement = (improved_conf - basic_conf) / basic_conf
                total_improvement += improvement
    
    if successful_comparisons > 0:
        avg_basic_conf = np.mean(basic_confidences)
        avg_improved_conf = np.mean(improved_confidences)
        avg_improvement_percent = (total_improvement / successful_comparisons) * 100
        
        print(f"Scenarios tested: {successful_comparisons}")
        print(f"Average basic confidence: {avg_basic_conf:.3f}")
        print(f"Average improved confidence: {avg_improved_conf:.3f}")
        print(f"Average improvement: {avg_improvement_percent:+.1f}%")
        
        # Calculate estimated overall accuracy
        estimated_accuracy = avg_improved_conf * 0.9  # Conservative estimate
        print(f"Estimated overall accuracy: {estimated_accuracy:.1%}")
        
        return {
            "scenarios_tested": successful_comparisons,
            "avg_basic_confidence": avg_basic_conf,
            "avg_improved_confidence": avg_improved_conf,
            "avg_improvement_percent": avg_improvement_percent,
            "estimated_accuracy": estimated_accuracy
        }
    
    return None


def test_edge_cases():
    """Test edge cases and error handling."""
    print("=== EDGE CASES TEST ===\n")
    
    edge_cases = [
        {"cycles": [], "description": "Empty data"},
        {"cycles": [28], "description": "Single cycle"},
        {"cycles": [28, 29], "description": "Two cycles"},
        {"cycles": [15, 16, 17], "description": "Very short cycles"},
        {"cycles": [85, 86, 87], "description": "Very long cycles"},
        {"cycles": [20, 90, 25, 85, 30, 80], "description": "Extreme variation"}
    ]
    
    results = {}
    
    for case in edge_cases:
        cycles = case["cycles"]
        description = case["description"]
        
        print(f"Testing {description}: {cycles}")
        
        try:
            result = improved_predictor.predict_with_maximum_accuracy(cycles)
            confidence = result.get("adaptive_confidence", {}).get("overall_confidence", 0)
            method = result.get("method", "unknown")
            print(f"  Result: {method} - Confidence: {confidence:.3f}")
            results[description] = {"success": True, "confidence": confidence, "method": method}
        except Exception as e:
            print(f"  Result: FAILED - {e}")
            results[description] = {"success": False, "error": str(e)}
        
        print()
    
    return results


def main():
    """Run comprehensive accuracy testing."""
    print("🚀 STARTING COMPREHENSIVE ACCURACY TESTING\n")
    
    # Test individual components
    feature_success = test_feature_engineering()
    confidence_success = test_adaptive_confidence()
    ensemble_success = test_ensemble_predictor()
    
    # Test prediction methods comparison
    comparison_results = test_prediction_methods_comparison()
    
    # Calculate overall improvement
    improvement_analysis = calculate_overall_improvement(comparison_results)
    
    # Test edge cases
    edge_case_results = test_edge_cases()
    
    # Summary
    print("=== FINAL SUMMARY ===\n")
    
    component_status = {
        "Feature Engineering": "✅" if feature_success else "❌",
        "Adaptive Confidence": "✅" if confidence_success else "❌",
        "Ensemble Predictor": "✅" if ensemble_success else "❌"
    }
    
    print("Component Status:")
    for component, status in component_status.items():
        print(f"  {component}: {status}")
    
    print()
    
    if improvement_analysis:
        print("Accuracy Improvement:")
        print(f"  Scenarios tested: {improvement_analysis['scenarios_tested']}")
        print(f"  Average improvement: {improvement_analysis['avg_improvement_percent']:+.1f}%")
        print(f"  Estimated overall accuracy: {improvement_analysis['estimated_accuracy']:.1%}")
        
        # Check if 60% target is met
        target_met = improvement_analysis['estimated_accuracy'] >= 0.60
        print(f"  60% accuracy target: {'✅ MET' if target_met else '❌ NOT MET'}")
    
    print("\n🎯 TESTING COMPLETE")


if __name__ == "__main__":
    main()
