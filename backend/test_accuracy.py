"""
Test current model accuracy and identify improvement areas.
"""
import numpy as np
from app.services.ml_predictor import predict_next_cycles
from app.services.enhanced_predictor import enhanced_predictor
from app.services.pcod_risk import compute_pcod_risk
from app.services.stress_analyzer import calculate_stress_score

def generate_test_data():
    """Generate realistic test data for accuracy evaluation."""
    np.random.seed(42)
    
    # Regular cycles (28±2 days)
    regular_cycles = [28, 29, 27, 28, 30, 26, 28, 29, 27, 28, 29, 28]
    
    # Irregular cycles (high variance)
    irregular_cycles = [25, 35, 22, 40, 28, 45, 20, 38, 26, 42, 24, 36]
    
    # PCOD-like patterns (long and irregular)
    pcod_cycles = [35, 42, 28, 45, 38, 50, 32, 48, 40, 55, 35, 46]
    
    # Trending longer cycles
    trending_cycles = [26, 27, 28, 30, 32, 34, 35, 37, 38, 40, 42, 44]
    
    return {
        "regular": regular_cycles,
        "irregular": irregular_cycles,
        "pcod": pcod_cycles,
        "trending": trending_cycles
    }

def test_prediction_accuracy():
    """Test prediction accuracy on different patterns."""
    test_data = generate_test_data()
    results = {}
    
    for pattern_name, cycles in test_data.items():
        print(f"\n=== Testing {pattern_name.upper()} pattern ===")
        print(f"Input cycles: {cycles}")
        
        # Test basic predictor
        basic_pred = predict_next_cycles(cycles)
        print(f"Basic method: {basic_pred['method']}")
        print(f"Overall confidence: {basic_pred.get('overall_confidence', 0):.2f}")
        
        # Test enhanced predictor
        enhanced_pred = enhanced_predictor.predict_with_insights(cycles)
        pattern_analysis = enhanced_pred.get('pattern_analysis', {})
        risk_assessment = enhanced_pred.get('risk_indicators', {})
        quality_assessment = enhanced_pred.get('prediction_quality', {})
        
        print(f"Detected patterns: {pattern_analysis.get('detected_patterns', [])}")
        print(f"Risk level: {risk_assessment.get('risk_level', 'unknown')}")
        print(f"Prediction quality: {quality_assessment.get('quality_score', 0):.2f}")
        print(f"Reliability: {quality_assessment.get('reliability', 'unknown')}")
        
        results[pattern_name] = {
            'basic': basic_pred,
            'enhanced': enhanced_pred,
            'input_cycles': cycles
        }
    
    return results

def test_stress_analysis():
    """Test stress analysis accuracy."""
    print("\n=== Testing Stress Analysis ===")
    
    # Test cases with known stress levels
    test_cases = [
        {
            "name": "High Stress Case",
            "data": {
                "stress": 8,
                "sleep_hours": 5,
                "exercise": "none",
                "mood": "anxious",
                "symptoms": ["headache", "muscle_tension"],
                "notes": "I feel overwhelmed and anxious about work"
            }
        },
        {
            "name": "Low Stress Case",
            "data": {
                "stress": 2,
                "sleep_hours": 8,
                "exercise": "moderate",
                "mood": "happy",
                "symptoms": [],
                "notes": "Feeling great and relaxed today"
            }
        },
        {
            "name": "Medium Stress Case",
            "data": {
                "stress": 5,
                "sleep_hours": 6,
                "exercise": "light",
                "mood": "tired",
                "symptoms": ["fatigue"],
                "notes": "A bit concerned about upcoming deadlines"
            }
        }
    ]
    
    for case in test_cases:
        stress_result = calculate_stress_score(case["data"])
        print(f"\n{case['name']}:")
        print(f"  Predicted stress: {stress_result['stress_score']}/10")
        print(f"  Stress level: {stress_result['stress_level']}")
        print(f"  Confidence factors: {len(stress_result['weighted_components'])}")

def test_pcod_risk():
    """Test PCOD risk assessment."""
    print("\n=== Testing PCOD Risk Assessment ===")
    
    # Test cases
    test_cases = [
        {
            "name": "Normal cycles",
            "cycles": [
                {"start_date": "2024-01-01", "symptoms": ["cramps"], "mood": "normal"},
                {"start_date": "2024-01-29", "symptoms": ["headache"], "mood": "tired"},
                {"start_date": "2024-02-26", "symptoms": ["cramps"], "mood": "normal"}
            ]
        },
        {
            "name": "PCOD-like cycles",
            "cycles": [
                {"start_date": "2024-01-01", "symptoms": ["acne", "weight gain", "hairfall"], "mood": "irritable"},
                {"start_date": "2024-02-15", "symptoms": ["acne", "fatigue"], "mood": "anxious"},
                {"start_date": "2024-04-05", "symptoms": ["hairfall", "weight gain"], "mood": "depressed"}
            ]
        }
    ]
    
    for case in test_cases:
        risk_result = compute_pcod_risk(case["cycles"])
        print(f"\n{case['name']}:")
        print(f"  Risk score: {risk_result['risk_score']}/100")
        print(f"  Risk level: {risk_result['level']}")
        print(f"  Factors: {len(risk_result['factors'])}")

def calculate_current_accuracy():
    """Calculate current system accuracy metrics."""
    print("\n=== CURRENT ACCURACY ANALYSIS ===")
    
    # Test predictions
    pred_results = test_prediction_accuracy()
    
    # Calculate accuracy metrics
    total_confidence = 0
    total_quality = 0
    pattern_count = 0
    
    for pattern, results in pred_results.items():
        basic_conf = results['basic'].get('overall_confidence', 0)
        enhanced_quality = results['enhanced'].get('prediction_quality', {}).get('quality_score', 0)
        
        total_confidence += basic_conf
        total_quality += enhanced_quality
        pattern_count += 1
        
        print(f"{pattern}: Basic Conf={basic_conf:.2f}, Enhanced Quality={enhanced_quality:.2f}")
    
    avg_confidence = total_confidence / pattern_count if pattern_count > 0 else 0
    avg_quality = total_quality / pattern_count if pattern_count > 0 else 0
    
    print(f"\nAverage Basic Confidence: {avg_confidence:.2f}")
    print(f"Average Enhanced Quality: {avg_quality:.2f}")
    
    # Test other components
    test_stress_analysis()
    test_pcod_risk()
    
    # Overall accuracy estimate
    overall_accuracy = (avg_confidence + avg_quality) / 2
    print(f"\n=== ESTIMATED CURRENT ACCURACY: {overall_accuracy:.1%} ===")
    
    return {
        "avg_confidence": avg_confidence,
        "avg_quality": avg_quality,
        "overall_accuracy": overall_accuracy
    }

if __name__ == "__main__":
    calculate_current_accuracy()
