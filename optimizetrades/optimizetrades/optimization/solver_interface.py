"""Solver interface wraps cvxpy Problem.solve with sensible defaults."""
from __future__ import annotations

from typing import Any, Dict, Optional

import cvxpy as cp

# Preference order – if a solver isn't installed we'll fall through to the next.
_SOLVERS: Dict[str, str] = {
    "ECOS": cp.ECOS,
    "OSQP": cp.OSQP,
    "SCS": cp.SCS,
}


def solve_problem(problem: cp.Problem, solver: str | None = None, **kwargs) -> Dict[str, Any]:
    """Solve *problem* and return diagnostic results.

    Parameters
    ----------
    problem : cvxpy.Problem
        Convex optimisation problem.
    solver : str, optional
        Solver key in ``_SOLVERS``. Falls back to ECOS.

    Returns
    -------
    dict
        status, objective value, solver_stats.
    """
    # Determine the solver to use.
    if solver is not None:
        # Respect explicit request and let cvxpy raise if unavailable.
        chosen_solver = _SOLVERS.get(solver.upper(), solver)
    else:
        # Pick the first solver in _SOLVERS that is actually installed.
        installed = set(cp.installed_solvers())
        for name, const in _SOLVERS.items():
            if const in installed:
                chosen_solver = const
                break
        else:
            # Fallback to whatever default cvxpy thinks is best.
            chosen_solver = None  # type: ignore[assignment]

    result = problem.solve(solver=chosen_solver, **kwargs)

    stats = {
        "status": problem.status,
        "objective_value": problem.value,
        "solver_stats": problem.solver_stats.__dict__,
    }
    return {"result": result, **stats} 