"""
LSTM-based next-cycle prediction (3 future cycles) with simple confidence bands.
Falls back to moving-average + variance if the model file is missing.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

# Lazy TF import to allow running API without full TF on very constrained envs
_model = None
_SEQ_LEN = 6


def _model_path() -> Path:
    base = Path(__file__).resolve().parent.parent.parent
    return base / "models" / "cycle_lstm.keras"


def _load_keras_model():
    global _model
    if _model is not None:
        return _model
    p = _model_path()
    if not p.exists():
        return None
    try:
        import tensorflow as tf  # noqa: WPS433
    except ImportError:  # pragma: no cover
        return None

    _model = tf.keras.models.load_model(p, compile=False)
    return _model


def _prepare_sequence(cycle_days: List[float]) -> np.ndarray:
    if len(cycle_days) < 2:
        return np.array([])
    # Pad left with median for fixed length
    seq = list(cycle_days[-_SEQ_LEN :])
    while len(seq) < _SEQ_LEN:
        seq.insert(0, float(np.median(cycle_days)))
    arr = np.array(seq, dtype=np.float32).reshape(1, _SEQ_LEN, 1)
    return arr / 35.0  # scale roughly to network range


def _ma_fallback(
    cycle_days: List[int],
) -> Tuple[List[Dict[str, Any]], float]:
    if len(cycle_days) < 1:
        return [], 0.0
    last = [float(c) for c in cycle_days]
    mean = float(np.mean(last))
    std = float(np.std(last)) if len(last) > 1 else 5.0
    preds: List[Dict[str, Any]] = []
    cur = last[-1]
    for k in range(1, 4):
        nxt = 0.7 * mean + 0.3 * cur
        lo = max(15.0, nxt - 1.2 * std)
        hi = min(90.0, nxt + 1.2 * std)
        conf = max(0.2, 1.0 - min(1.0, std / 20.0))
        preds.append(
            {
                "cycle_index": k,
                "predicted_length_days": round(nxt, 1),
                "interval_low": round(lo, 1),
                "interval_high": round(hi, 1),
                "confidence": round(conf, 2),
            }
        )
        cur = nxt
    overall_conf = float(np.mean([p["confidence"] for p in preds])) if preds else 0.0
    return preds, overall_conf


def predict_next_cycles(
    cycle_lengths: List[int],
) -> Dict[str, Any]:
    if len(cycle_lengths) < 1:
        return {
            "method": "none",
            "next_cycles": [],
            "confidence_interval": [0, 0],
            "message": "Need at least one logged cycle for a baseline; two or more improve accuracy.",
        }

    cy = [float(c) for c in cycle_lengths]
    m = _load_keras_model()
    if m is None or len(cy) < 2:
        nxt, conf = _ma_fallback(cycle_lengths)
        return {
            "method": "moving_average" if m is None else "lstm",
            "next_cycles": nxt,
            "overall_confidence": conf,
        }

    try:
        x = _prepare_sequence(cy)
        if x.size == 0:
            nxt, conf = _ma_fallback(cycle_lengths)
            return {
                "method": "hybrid",
                "next_cycles": nxt,
                "overall_confidence": conf,
            }
        out = m.predict(x, verbose=0)
        # Model outputs 3 day lengths
        if out.ndim == 1:
            raw = out[:3]
        else:
            raw = out[0, :3]
        preds: List[Dict[str, Any]] = []
        std = float(np.std(cy)) if len(cy) > 1 else 5.0
        for k, val in enumerate(raw, start=1):
            nxt = float(val) * 35.0  # inverse scale
            nxt = max(15.0, min(90.0, nxt))
            preds.append(
                {
                    "cycle_index": k,
                    "predicted_length_days": round(nxt, 1),
                    "interval_low": round(max(15.0, nxt - 1.0 * std), 1),
                    "interval_high": round(min(90.0, nxt + 1.0 * std), 1),
                    "confidence": round(
                        max(0.2, 1.0 - min(1.0, std / 22.0)), 2
                    ),
                }
            )
        oconf = float(np.mean([p["confidence"] for p in preds])) if preds else 0.0
        return {
            "method": "lstm",
            "next_cycles": preds,
            "overall_confidence": oconf,
        }
    except Exception:
        nxt, conf = _ma_fallback(cycle_lengths)
        return {
            "method": "fallback_ma",
            "next_cycles": nxt,
            "overall_confidence": conf,
        }
