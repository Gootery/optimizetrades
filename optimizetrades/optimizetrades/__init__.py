"""optimizetrades top-level."""

__all__ = [
    "version",
    "optimize_markowitz",
]

version: str = "0.1.0"

# Convenience re-export
from optimizetrades.optimization.qp_markowitz import optimize_markowitz  # noqa: E402 