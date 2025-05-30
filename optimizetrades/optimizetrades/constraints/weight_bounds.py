"""Weight bound constraint."""
from __future__ import annotations

from typing import Tuple

import cvxpy as cp

from optimizetrades.constraints.base import Constraint


class WeightBounds(Constraint):
    """Simple box constraints ``min_w ≤ w_i ≤ max_w`` for each asset."""

    def __init__(self, bounds: Tuple[float, float] = (0.0, 0.1)) -> None:  # noqa: D401
        self.lower, self.upper = bounds

    def cvxpy_constr(self, weight_var: cp.Variable, aux_data=None):  # noqa: D401
        return [weight_var >= self.lower, weight_var <= self.upper] 