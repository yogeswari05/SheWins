"""
Transformer-based next-cycle prediction (3 future cycles) with confidence bands.
Falls back to moving-average + variance if the model file is missing.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple
import pickle

import numpy as np

# Lazy TF import to allow running API without full TF on very constrained envs
_model = None
_scaler_X = None
_scaler_y = None
_SEQ_LEN = 8
N_FEATURES = 4

def _models_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "models"

def _model_path() -> Path:
    return _models_dir() / "cycle_transformer.keras"

def _load_keras_model():
    global _model, _scaler_X, _scaler_y
    if _model is not None:
        return _model
    p = _model_path()
    if not p.exists():
        return None
    try:
        import tensorflow as tf
    except ImportError:
        return None

    _model = tf.keras.models.load_model(p, compile=False)
    
    # Load scalers
    try:
        with open(_models_dir() / "scaler_X.pkl", "rb") as f:
            _scaler_X = pickle.load(f)
        with open(_models_dir() / "scaler_y.pkl", "rb") as f:
            _scaler_y = pickle.load(f)
    except:
        pass # Handle case where scalers might not be there gracefully
        
    return _model

def _prepare_sequence(cycle_days: List[float], cycles_data: Optional[List[Dict[str, Any]]] = None) -> np.ndarray:
    if len(cycle_days) < 2:
        return np.array([])
        
    # Extract covariates if data is provided
    sleep_seq = []
    stress_seq = []
    symp_seq = []
    
    if cycles_data and len(cycles_data) == len(cycle_days):
        for c in cycles_data:
            sleep = float(c.get("sleep_hours") or 7.0)
            stress = float(c.get("stress") or 5.0)
            symps = len(c.get("symptoms") or [])
            symp_val = float(min(10, symps * 2))
            
            sleep_seq.append(sleep)
            stress_seq.append(stress)
            symp_seq.append(symp_val)
    else:
        sleep_seq = [7.0] * len(cycle_days)
        stress_seq = [5.0] * len(cycle_days)
        symp_seq = [2.0] * len(cycle_days)
        
    # Pad left with median for fixed length
    seq = list(cycle_days[-_SEQ_LEN :])
    slp = list(sleep_seq[-_SEQ_LEN :])
    str_s = list(stress_seq[-_SEQ_LEN :])
    sym = list(symp_seq[-_SEQ_LEN :])
    
    while len(seq) < _SEQ_LEN:
        seq.insert(0, float(np.median(cycle_days)))
        slp.insert(0, 7.0)
        str_s.insert(0, 5.0)
        sym.insert(0, 2.0)
        
    arr = np.zeros((1, _SEQ_LEN, N_FEATURES), dtype=np.float32)
    for j in range(_SEQ_LEN):
        arr[0, j, 0] = seq[j]
        arr[0, j, 1] = slp[j]
        arr[0, j, 2] = str_s[j]
        arr[0, j, 3] = sym[j]
        
    global _scaler_X
    if _scaler_X is not None:
        flat_arr = arr.reshape(-1, N_FEATURES)
        arr = _scaler_X.transform(flat_arr).reshape(1, _SEQ_LEN, N_FEATURES)
        
    return arr

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
    cycles_data: Optional[List[Dict[str, Any]]] = None
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
            "method": "moving_average" if m is None else "transformer",
            "next_cycles": nxt,
            "overall_confidence": conf,
        }

    try:
        x = _prepare_sequence(cy, cycles_data)
        if x.size == 0:
            nxt, conf = _ma_fallback(cycle_lengths)
            return {
                "method": "hybrid",
                "next_cycles": nxt,
                "overall_confidence": conf,
            }
        out = m.predict(x, verbose=0)
        
        global _scaler_y
        if _scaler_y is not None:
            out = _scaler_y.inverse_transform(out)
            
        if out.ndim == 1:
            raw = out[:3]
        else:
            raw = out[0, :3]
            
        preds: List[Dict[str, Any]] = []
        std = float(np.std(cy)) if len(cy) > 1 else 5.0
        for k, val in enumerate(raw, start=1):
            nxt = float(val) 
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
            "method": "transformer",
            "next_cycles": preds,
            "overall_confidence": oconf,
        }
    except Exception as e:
        nxt, conf = _ma_fallback(cycle_lengths)
        return {
            "method": "fallback_ma",
            "next_cycles": nxt,
            "overall_confidence": conf,
        }
