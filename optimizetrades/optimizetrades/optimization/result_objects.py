"""Small dataclasses for optimisation results."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np
import pandas as pd


@dataclass
class OptimResult:
    """Single optimise run."""

    weights: pd.Series  # index tickers, values weights
    expected_return: float
    volatility: float
    diagnostics: Dict[str, object]

    def to_dict(self) -> Dict[str, object]:  # noqa: D401
        return {
            "weights": self.weights.to_dict(),
            "expected_return": self.expected_return,
            "volatility": self.volatility,
            "diagnostics": self.diagnostics,
        }


@dataclass
class FrontierResult:
    """Efficient frontier."""

    returns: np.ndarray
    vols: np.ndarray
    weights: np.ndarray  # shape (n_portfolios, n_assets) 