"""Base class for optimisation constraints."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

import cvxpy as cp
import pandas as pd


class Constraint(ABC):
    """Shared bits for concrete constraints.

    Subclasses just implement ``cvxpy_constr``.
    """

    @abstractmethod
    def cvxpy_constr(self, weight_var: cp.Variable, aux_data: Dict[str, Any] | None = None):
        """Return cvxpy constraint list."""
        raise NotImplementedError

    # Utility helper so constraints can reference price / exposures frames
    def set_data(self, data: Dict[str, pd.DataFrame] | None = None) -> None:  # noqa: D401
        """Store any aux data we might need."""
        self._data = data or {}

    # Allow clean string representation
    def __repr__(self) -> str:  # noqa: D401
        return f"<{self.__class__.__name__}>" 