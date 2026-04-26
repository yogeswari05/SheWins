"""Scikit-learn helpers for irregularity / anomaly hints on cycle lengths."""
from __future__ import annotations

from typing import List

import numpy as np


def isolation_irregularity_score(lengths: List[int]) -> float | None:
    """Returns 0-1 irregularity hint; None if not enough data."""
    if len(lengths) < 4:
        return None
    try:
        from sklearn.ensemble import IsolationForest  # noqa: WPS433

        X = np.array(lengths, dtype=float).reshape(-1, 1)
        clf = IsolationForest(random_state=42, contamination="auto")
        clf.fit(X)
        pred = clf.predict(X)
        # fraction of points flagged as outliers
        frac = float(np.mean(pred == -1))
        return round(min(1.0, max(0.0, frac)), 3)
    except Exception:  # pragma: no cover
        return None
