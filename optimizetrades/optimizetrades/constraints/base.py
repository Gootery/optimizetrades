"""Abstract base class for constraints used in optimisation."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

import cvxpy as cp
import pandas as pd


class Constraint(ABC):
    """Base class for all constraints.

    Each subclass implements :py:meth:`cvxpy_constr` which converts the high-level
    constraint into one or more `cvxpy` constraints.
    """

    @abstractmethod
    def cvxpy_constr(self, weight_var: cp.Variable, aux_data: Dict[str, Any] | None = None):
        """Return a list of cvxpy constraints implementing the rule."""
        raise NotImplementedError

    # Utility helper so constraints can reference price / exposures frames
    def set_data(self, data: Dict[str, pd.DataFrame] | None = None) -> None:  # noqa: D401
        """Optionally store market data needed for the constraint."""
        self._data = data or {}

    # Allow clean string representation
    def __repr__(self) -> str:  # noqa: D401
        return f"<{self.__class__.__name__}>" 