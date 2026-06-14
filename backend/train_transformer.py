import os
import sys
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SEQ_LEN = 8
N_SAMPLES = 15000
N_FEATURES = 4  # cycle_length, sleep_hours, stress_level, symptom_severity

def generate_multivariate_data():
    """Generates synthetic data with covariates."""
    print("Generating multivariate training data...")
    rng = np.random.default_rng(42)
    
    X = np.zeros((N_SAMPLES, SEQ_LEN, N_FEATURES), dtype=np.float32)
    y = np.zeros((N_SAMPLES, 3), dtype=np.float32)
    
    for i in range(N_SAMPLES):
        pattern_type = rng.choice(['regular', 'irregular', 'pcod_like'], p=[0.5, 0.3, 0.2])
        
        sequence = []
        sleep_seq = []
        stress_seq = []
        symptom_seq = []
        
        if pattern_type == 'regular':
            base_cycle = rng.uniform(26, 32)
            volatility = rng.uniform(1, 3)
            base_sleep = rng.uniform(6.5, 8.5)
            base_stress = rng.uniform(1, 4)
            base_symp = rng.uniform(1, 3)
        elif pattern_type == 'irregular':
            base_cycle = rng.uniform(20, 45)
            volatility = rng.uniform(5, 12)
            base_sleep = rng.uniform(5.0, 7.5)
            base_stress = rng.uniform(4, 8)
            base_symp = rng.uniform(4, 7)
        else: # pcod_like
            base_cycle = rng.uniform(35, 60)
            volatility = rng.uniform(10, 20)
            base_sleep = rng.uniform(4.0, 7.0)
            base_stress = rng.uniform(6, 10)
            base_symp = rng.uniform(6, 10)
            
        for j in range(SEQ_LEN):
            cycle_val = base_cycle + rng.normal(0, volatility)
            # Higher stress and lower sleep correlate with longer cycles and more symptoms
            sleep_val = max(0, min(12, base_sleep + rng.normal(0, 1)))
            stress_val = max(0, min(10, base_stress + rng.normal(0, 2)))
            symp_val = max(0, min(10, base_symp + (stress_val * 0.2) - (sleep_val * 0.1) + rng.normal(0, 1)))
            
            # Simple heuristic correlation: high stress -> longer cycle
            cycle_val += (stress_val - 5) * 1.5
            cycle_val = max(15, min(90, cycle_val))
            
            sequence.append(cycle_val)
            sleep_seq.append(sleep_val)
            stress_seq.append(stress_val)
            symptom_seq.append(symp_val)
            
        # Target is next 3 cycles
        n1 = sequence[-1] + (stress_seq[-1] - 5) * 1.5 + rng.normal(0, volatility)
        n2 = n1 + rng.normal(0, volatility)
        n3 = n2 + rng.normal(0, volatility)
        
        n1 = max(15, min(90, n1))
        n2 = max(15, min(90, n2))
        n3 = max(15, min(90, n3))
        
        for j in range(SEQ_LEN):
            X[i, j, 0] = sequence[j]
            X[i, j, 1] = sleep_seq[j]
            X[i, j, 2] = stress_seq[j]
            X[i, j, 3] = symptom_seq[j]
            
        y[i] = [n1, n2, n3]
        
    return X, y

def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
    # Attention and Normalization
    x = layers.MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(inputs, inputs)
    x = layers.Dropout(dropout)(x)
    x = layers.LayerNormalization(epsilon=1e-6)(x)
    res = x + inputs

    # Feed Forward Part
    x = layers.Conv1D(filters=ff_dim, kernel_size=1, activation="relu")(res)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    x = layers.LayerNormalization(epsilon=1e-6)(x)
    return x + res

def build_model(
    input_shape,
    head_size,
    num_heads,
    ff_dim,
    num_transformer_blocks,
    mlp_units,
    dropout=0,
    mlp_dropout=0,
):
    inputs = tf.keras.Input(shape=input_shape)
    x = inputs
    
    for _ in range(num_transformer_blocks):
        x = transformer_encoder(x, head_size, num_heads, ff_dim, dropout)

    x = layers.GlobalAveragePooling1D(data_format="channels_first")(x)
    
    for dim in mlp_units:
        x = layers.Dense(dim, activation="relu")(x)
        x = layers.Dropout(mlp_dropout)(x)
        
    outputs = layers.Dense(3, activation="linear")(x)
    return tf.keras.Model(inputs, outputs)

def train():
    X, y = generate_multivariate_data()
    
    # Flatten X to scale, then reshape
    X_flat = X.reshape(-1, N_FEATURES)
    scaler_X = StandardScaler()
    X_scaled = scaler_X.fit_transform(X_flat).reshape(-1, SEQ_LEN, N_FEATURES)
    
    scaler_y = StandardScaler()
    y_scaled = scaler_y.fit_transform(y)
    
    # Save scalers
    models_dir = HERE / "models"
    models_dir.mkdir(exist_ok=True)
    with open(models_dir / "scaler_X.pkl", "wb") as f:
        pickle.dump(scaler_X, f)
    with open(models_dir / "scaler_y.pkl", "wb") as f:
        pickle.dump(scaler_y, f)
        
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
    
    input_shape = X_train.shape[1:]

    model = build_model(
        input_shape,
        head_size=32,
        num_heads=4,
        ff_dim=64,
        num_transformer_blocks=2,
        mlp_units=[64, 32],
        mlp_dropout=0.2,
        dropout=0.1,
    )

    model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), metrics=["mae"])
    model.summary()

    callbacks_list = [
        tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=4)
    ]

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=64,
        callbacks=callbacks_list,
    )

    model.save(models_dir / "cycle_transformer.keras")
    print(f"Model saved to {models_dir / 'cycle_transformer.keras'}")

if __name__ == "__main__":
    train()
