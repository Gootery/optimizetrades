"""Basic smoke test for Markowitz optimisation."""
import numpy as np
import pandas as pd

from optimizetrades.optimization.qp_markowitz import optimize_markowitz


def test_optimize_markowitz_smoke():
    rng = np.random.default_rng(42)
    n = 5
    mu = pd.Series(rng.normal(0.05, 0.02, size=n), index=[f"Asset{i}" for i in range(n)])
    A = rng.normal(size=(n, n))
    cov = pd.DataFrame(A @ A.T, index=mu.index, columns=mu.index)  # SPD

    result = optimize_markowitz(mu, cov)
    w = result.weights

    # Weights sum to 1 and are finite
    assert np.isclose(w.sum(), 1.0, atol=1e-6)
    assert np.all(np.isfinite(w)) 