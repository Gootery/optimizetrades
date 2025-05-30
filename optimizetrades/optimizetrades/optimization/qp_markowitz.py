"""Mean–variance optimisation via quadratic programming (Markowitz)."""
from __future__ import annotations

from typing import List, Sequence

import cvxpy as cp
import numpy as np
import pandas as pd

from optimizetrades.constraints.base import Constraint
from optimizetrades.optimization.result_objects import OptimResult
from optimizetrades.optimization.solver_interface import solve_problem


def optimize_markowitz(
    mu: pd.Series,
    cov: pd.DataFrame,
    risk_aversion: float = 1.0,
    constraints: Sequence[Constraint] | None = None,
    solver: str | None = None,
) -> OptimResult:
    """Compute the tangency portfolio that maximises µᵀw − λ wᵀΣw.

    Parameters
    ----------
    mu : pd.Series
        Expected returns (index tickers).
    cov : pd.DataFrame
        Covariance matrix aligned with *mu*.
    risk_aversion : float, default 1.0
        λ in the objective. Higher = more risk‐averse (shrinks toward min‐var).
    constraints : sequence[Constraint], optional
        Additional constraints. Implicitly enforces ∑w = 1.
    solver : str, optional
        Solver key recognised by ``solve_problem``.

    Returns
    -------
    OptimResult
    """
    tickers: List[str] = list(mu.index)
    n = len(tickers)

    # Decision variable
    w = cp.Variable(n)

    # Objective: maximise expected utility → minimise negative (cvxpy minimises)
    obj = cp.Maximize(mu.values @ w - risk_aversion * cp.quad_form(w, cov.values))

    # Base constraints (fully invested)
    constr = [cp.sum(w) == 1]

    # Apply user constraints
    for c in constraints or []:
        constr += list(c.cvxpy_constr(w))

    problem = cp.Problem(obj, constr)
    diag = solve_problem(problem, solver=solver)

    weights = pd.Series(w.value, index=tickers)
    port_mu = float(mu @ weights)
    port_vol = float(np.sqrt(weights @ cov.values @ weights))
    result = OptimResult(weights, port_mu, port_vol, diagnostics=diag)

    return result 