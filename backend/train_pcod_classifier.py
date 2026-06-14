import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

N_SAMPLES = 5000

def generate_pcod_data():
    """Generates synthetic tabular data for PCOD risk classification."""
    print("Generating PCOD synthetic dataset...")
    rng = np.random.default_rng(42)
    
    data = []
    for _ in range(N_SAMPLES):
        # Base probabilities
        is_pcod = rng.choice([0, 1], p=[0.7, 0.3])
        
        if is_pcod:
            cycle_variance = rng.normal(25, 10)  # High variance
            max_gap = rng.normal(55, 15)         # Long gaps
            acne_severity = rng.integers(4, 10)
            weight_gain_score = rng.integers(4, 10)
            hairfall_score = rng.integers(3, 10)
            fatigue_score = rng.integers(4, 10)
        else:
            cycle_variance = rng.normal(5, 3)    # Low variance
            max_gap = rng.normal(30, 5)          # Normal gaps
            acne_severity = rng.integers(0, 5)
            weight_gain_score = rng.integers(0, 5)
            hairfall_score = rng.integers(0, 5)
            fatigue_score = rng.integers(1, 6)
            
        # Ensure non-negative
        cycle_variance = max(0, cycle_variance)
        max_gap = max(15, max_gap)
        
        data.append({
            'cycle_variance': cycle_variance,
            'max_cycle_gap': max_gap,
            'acne_severity': acne_severity,
            'weight_gain_score': weight_gain_score,
            'hairfall_score': hairfall_score,
            'fatigue_score': fatigue_score,
            'is_pcod': is_pcod
        })
        
    return pd.DataFrame(data)

def train_classifier():
    df = generate_pcod_data()
    
    features = [
        'cycle_variance', 'max_cycle_gap', 'acne_severity',
        'weight_gain_score', 'hairfall_score', 'fatigue_score'
    ]
    
    X = df[features]
    y = df['is_pcod']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    models_dir = HERE / "models"
    models_dir.mkdir(exist_ok=True)
    with open(models_dir / "pcod_rf_model.pkl", "wb") as f:
        pickle.dump(clf, f)
        
    print(f"PCOD Model saved to {models_dir / 'pcod_rf_model.pkl'}")

if __name__ == "__main__":
    train_classifier()
