"""Top-level package for optimizetrades.

Exposes commonly-used functions directly at the package level for convenience.
"""

__all__ = [
    "version",
    "optimize_markowitz",
]

version: str = "0.1.0"

# Convenience re-export
from optimizetrades.optimization.qp_markowitz import optimize_markowitz  # noqa: E402 