"""Thin wrapper around ``problem.solve`` with nicer defaults."""
from __future__ import annotations

from typing import Any, Dict, Optional

import cvxpy as cp

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
    # pick solver (use request if given)
    if solver is not None:
        chosen_solver = _SOLVERS.get(solver.upper(), solver)
    else:
        # otherwise take first installed one
        installed = set(cp.installed_solvers())
        for name, const in _SOLVERS.items():
            if const in installed:
                chosen_solver = const
                break
        else:
            # nothing found – let cvxpy decide
            chosen_solver = None  # type: ignore[assignment]

    result = problem.solve(solver=chosen_solver, **kwargs)

    stats = {
        "status": problem.status,
        "objective_value": problem.value,
        "solver_stats": problem.solver_stats.__dict__,
    }
    return {"result": result, **stats} 