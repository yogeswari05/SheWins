"""
Enhanced LSTM training with improved architecture and data augmentation.
Run from `backend/`: python train_enhanced_lstm.py
Outputs: `models/enhanced_cycle_lstm.keras`
"""
import os
import sys
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

# Ensure we can import app
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SEQ_LEN = 8
N_SAMPLES = 15000
N_FEATURES = 3  # cycle_length, trend, volatility
RNG = np.random.default_rng(42)


def generate_realistic_data():
    """Generate more realistic training data with multiple patterns."""
    print("Generating realistic training data...")
    
    X = np.zeros((N_SAMPLES, SEQ_LEN, N_FEATURES), dtype=np.float32)
    y = np.zeros((N_SAMPLES, 3), dtype=np.float32)
    
    for i in range(N_SAMPLES):
        # Choose pattern type
        pattern_type = RNG.choice(['regular', 'irregular', 'trending', 'seasonal', 'pcod_like'], 
                                 p=[0.3, 0.25, 0.2, 0.15, 0.1])
        
        if pattern_type == 'regular':
            # Regular cycles with small variations
            base_cycle = RNG.uniform(26, 32)
            trend = RNG.normal(0, 0.5)
            volatility = RNG.uniform(1, 3)
            
        elif pattern_type == 'irregular':
            # Irregular cycles with high variations
            base_cycle = RNG.uniform(20, 45)
            trend = RNG.normal(0, 2)
            volatility = RNG.uniform(5, 15)
            
        elif pattern_type == 'trending':
            # Trending cycles
            base_cycle = RNG.uniform(25, 35)
            trend = RNG.choice([-1, 1]) * RNG.uniform(0.5, 2)
            volatility = RNG.uniform(2, 6)
            
        elif pattern_type == 'seasonal':
            # Seasonal patterns
            base_cycle = RNG.uniform(27, 33)
            trend = RNG.normal(0, 1)
            volatility = RNG.uniform(2, 5)
            # Add seasonal component
            seasonal_phase = RNG.uniform(0, 2 * np.pi)
            
        else:  # pcod_like
            # PCOD-like patterns (long and irregular)
            base_cycle = RNG.uniform(35, 50)
            trend = RNG.normal(0, 3)
            volatility = RNG.uniform(8, 20)
        
        # Generate sequence
        sequence = []
        for j in range(SEQ_LEN):
            if pattern_type == 'seasonal':
                seasonal_effect = 3 * np.sin(seasonal_phase + j * np.pi / 6)
                cycle_val = base_cycle + trend * j + seasonal_effect + RNG.normal(0, volatility)
            else:
                cycle_val = base_cycle + trend * j + RNG.normal(0, volatility)
            
            cycle_val = max(15, min(90, cycle_val))
            sequence.append(cycle_val)
        
        # Calculate features
        for j in range(SEQ_LEN):
            X[i, j, 0] = sequence[j] / 35.0  # normalized cycle length
            
            # Trend feature (local trend)
            if j >= 2:
                local_trend = (sequence[j] - sequence[j-2]) / 2
                X[i, j, 1] = local_trend / 5.0  # normalized trend
            else:
                X[i, j, 1] = 0.0
            
            # Volatility feature (local variance)
            if j >= 3:
                local_vol = np.std(sequence[max(0, j-3):j+1])
                X[i, j, 2] = local_vol / 10.0  # normalized volatility
            else:
                X[i, j, 2] = 0.1
        
        # Generate targets with more sophisticated logic
        last_cycle = sequence[-1]
        recent_avg = np.mean(sequence[-3:])
        overall_avg = np.mean(sequence)
        
        # Future predictions with pattern-specific logic
        if pattern_type == 'regular':
            # Regular: predict continuation with small variations
            n1 = 0.7 * recent_avg + 0.3 * last_cycle + RNG.normal(0, 1)
            n2 = 0.6 * recent_avg + 0.4 * n1 + RNG.normal(0, 1)
            n3 = 0.5 * recent_avg + 0.5 * n2 + RNG.normal(0, 1)
            
        elif pattern_type == 'irregular':
            # Irregular: more variance
            n1 = 0.6 * recent_avg + 0.4 * last_cycle + RNG.normal(0, 3)
            n2 = 0.5 * recent_avg + 0.5 * n1 + RNG.normal(0, 3)
            n3 = 0.4 * recent_avg + 0.6 * n2 + RNG.normal(0, 3)
            
        elif pattern_type == 'trending':
            # Trending: continue trend
            n1 = last_cycle + trend + RNG.normal(0, volatility * 0.5)
            n2 = n1 + trend + RNG.normal(0, volatility * 0.5)
            n3 = n2 + trend + RNG.normal(0, volatility * 0.5)
            
        elif pattern_type == 'seasonal':
            # Seasonal: continue seasonal pattern
            for k in range(1, 4):
                seasonal_effect = 3 * np.sin(seasonal_phase + (SEQ_LEN + k) * np.pi / 6)
                if k == 1:
                    n1 = last_cycle + trend + seasonal_effect + RNG.normal(0, volatility)
                elif k == 2:
                    n2 = n1 + trend + seasonal_effect + RNG.normal(0, volatility)
                else:
                    n3 = n2 + trend + seasonal_effect + RNG.normal(0, volatility)
                    
        else:  # pcod_like
            # PCOD-like: high variability with potential long cycles
            n1 = last_cycle + RNG.normal(0, volatility) + RNG.choice([-5, 0, 5, 10])
            n2 = n1 + RNG.normal(0, volatility) + RNG.choice([-3, 0, 3, 8])
            n3 = n2 + RNG.normal(0, volatility) + RNG.choice([-2, 0, 2, 6])
        
        # Normalize targets
        y[i] = np.array([n1, n2, n3]) / 35.0
    
    return X, y


def create_enhanced_model():
    """Create enhanced LSTM model with better architecture."""
    print("Creating enhanced LSTM model...")
    
    # Input layer
    inputs = layers.Input(shape=(SEQ_LEN, N_FEATURES))
    
    # First LSTM block with attention
    x = layers.LSTM(64, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)(inputs)
    x = layers.LayerNormalization()(x)
    
    # Second LSTM block
    x = layers.LSTM(32, return_sequences=True, dropout=0.2, recurrent_dropout=0.2)(x)
    x = layers.LayerNormalization()(x)
    
    # Third LSTM block
    x = layers.LSTM(16, return_sequences=False, dropout=0.2, recurrent_dropout=0.2)(x)
    x = layers.LayerNormalization()(x)
    
    # Dense layers with residual connections
    dense1 = layers.Dense(32, activation='relu')(x)
    dense1 = layers.Dropout(0.3)(dense1)
    
    dense2 = layers.Dense(16, activation='relu')(dense1)
    dense2 = layers.Dropout(0.2)(dense2)
    
    # Output layer
    outputs = layers.Dense(3, activation='linear')(dense2)
    
    model = models.Model(inputs=inputs, outputs=outputs)
    
    # Custom optimizer with learning rate schedule
    initial_lr = 0.001
    lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_lr, decay_steps=1000, decay_rate=0.9, staircase=True
    )
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)
    
    model.compile(
        optimizer=optimizer,
        loss='huber_loss',  # More robust to outliers
        metrics=['mae', 'mse']
    )
    
    return model


def train_model():
    """Train the enhanced model."""
    print("Starting enhanced LSTM training...")
    
    # Generate data
    X, y = generate_realistic_data()
    print(f"Generated {X.shape[0]} samples with {X.shape[1]} sequence length and {X.shape[2]} features")
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create model
    model = create_enhanced_model()
    model.summary()
    
    # Callbacks
    early_stopping = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=15,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=8,
        min_lr=1e-6,
        verbose=1
    )
    
    model_checkpoint = callbacks.ModelCheckpoint(
        HERE / "models" / "enhanced_cycle_lstm.keras",
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )
    
    # Train model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=64,
        callbacks=[early_stopping, reduce_lr, model_checkpoint],
        verbose=1
    )
    
    # Evaluate model
    val_loss, val_mae, val_mse = model.evaluate(X_val, y_val, verbose=0)
    print(f"Validation Loss: {val_loss:.4f}, MAE: {val_mae:.4f}, MSE: {val_mse:.4f}")
    
    # Save final model
    models_dir = HERE / "models"
    models_dir.mkdir(exist_ok=True)
    model.save(models_dir / "enhanced_cycle_lstm.keras")
    
    print(f"Enhanced model saved to {models_dir / 'enhanced_cycle_lstm.keras'}")
    
    return model, history


def test_model_performance():
    """Test the trained model performance."""
    print("\nTesting model performance...")
    
    # Load the best model
    model_path = HERE / "models" / "enhanced_cycle_lstm.keras"
    if model_path.exists():
        model = tf.keras.models.load_model(model_path)
        print("Loaded enhanced model for testing")
        
        # Generate test data
        X_test, y_test = generate_realistic_data()
        
        # Evaluate
        test_loss, test_mae, test_mse = model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {test_loss:.4f}, MAE: {test_mae:.4f}, MSE: {test_mse:.4f}")
        
        # Make some sample predictions
        sample_X = X_test[:5]
        sample_y = y_test[:5]
        predictions = model.predict(sample_X, verbose=0)
        
        print("\nSample predictions:")
        for i in range(5):
            print(f"Sample {i+1}:")
            print(f"  Actual: {[round(y * 35, 1) for y in sample_y[i]]}")
            print(f"  Predicted: {[round(p * 35, 1) for p in predictions[i]]}")
            print(f"  Error: {[round(abs(p - y) * 35, 1) for p, y in zip(predictions[i], sample_y[i])]}")
    else:
        print("No trained model found. Please train the model first.")


if __name__ == "__main__":
    model, history = train_model()
    test_model_performance()
