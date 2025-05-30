"""Sector concentration cap constraint."""
from __future__ import annotations

from typing import Dict

import cvxpy as cp
import numpy as np

from optimizetrades.constraints.base import Constraint


class SectorCap(Constraint):
    """Cap total weight allocated to each sector.

    Parameters
    ----------
    sector_map : dict[str, str]
        Mapping of *ticker* → *sector* label.
    max_sector_weight : float, default 0.25
        Maximum proportion of portfolio allowed in any single sector.
    """

    def __init__(self, sector_map: Dict[str, str], max_sector_weight: float = 0.25):
        self.sector_map = sector_map
        self.max_sector_weight = max_sector_weight

    def cvxpy_constr(self, weight_var: cp.Variable, aux_data=None):  # noqa: D401
        tickers = list(self.sector_map.keys())
        sectors = list(set(self.sector_map.values()))

        # Build sector exposure matrix S_{s,i} = 1 if asset i in sector s
        S = np.zeros((len(sectors), len(tickers)))
        for i, tkr in enumerate(tickers):
            s = sectors.index(self.sector_map[tkr])
            S[s, i] = 1.0

        return [S @ weight_var <= self.max_sector_weight] 