"""
Train a small LSTM to predict 3 future cycle lengths from the last 6.
Run from `backend/`:  python train_lstm.py
Outputs: `models/cycle_lstm.keras`
"""
import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

# Ensure we can import app
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import tensorflow as tf  # noqa: E402

SEQ = 6
N_SAMPLES = 8000
RNG = np.random.default_rng(42)


def synth_data():
    x = np.zeros((N_SAMPLES, SEQ, 1), dtype=np.float32)
    y = np.zeros((N_SAMPLES, 3), dtype=np.float32)
    for i in range(N_SAMPLES):
        drift = float(RNG.normal(0, 4))
        base = float(RNG.uniform(22, 40))
        seq = [max(15.0, min(90.0, base + RNG.normal(0, 3) * j * 0.1 + drift)) for j in range(6)]
        x[i, :, 0] = np.array(seq) / 35.0
        n1 = max(15.0, min(90.0, 0.6 * np.mean(seq) + 0.4 * seq[-1] + RNG.normal(0, 2)))
        n2 = max(15.0, min(90.0, 0.55 * n1 + 0.45 * seq[-1] + RNG.normal(0, 2)))
        n3 = max(15.0, min(90.0, 0.5 * n2 + 0.5 * n1 + RNG.normal(0, 2)))
        y[i] = np.array([n1, n2, n3]) / 35.0
    return x, y


def main():
    x, y = synth_data()
    m = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(SEQ, 1)),
            tf.keras.layers.LSTM(32, return_sequences=True),
            tf.keras.layers.LSTM(16),
            tf.keras.layers.Dense(3, activation="linear"),
        ]
    )
    m.compile(optimizer="adam", loss="mse", metrics=["mae"])
    m.fit(x, y, epochs=12, batch_size=64, validation_split=0.1, verbose=1)
    out_dir = HERE / "models"
    out_dir.mkdir(exist_ok=True)
    p = out_dir / "cycle_lstm.keras"
    m.save(p)
    print("Saved to", p)


if __name__ == "__main__":
    main()
