from __future__ import annotations

from datetime import date
from typing import List

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from optimizetrades.data.market_data import get_price_data
from optimizetrades.optimization.qp_markowitz import optimize_markowitz

app = FastAPI(title="optimizetrades", version="0.1.0")


# ------------------
# Pydantic Schemas
# ------------------
class OptimRequest(BaseModel):
    tickers: List[str] = Field(..., example=["AAPL", "MSFT", "GOOG"])
    start: date = Field(..., example="2020-01-01")
    end: date | None = Field(None, example="2024-01-01")
    risk_aversion: float = 1.0


class OptimResponse(BaseModel):
    weights: dict[str, float]
    expected_return: float
    volatility: float


# ------------------
# Routes
# ------------------
@app.post("/optimize", response_model=OptimResponse)
async def optimize_portfolio(req: OptimRequest):
    # pull prices
    price_df = get_price_data(req.tickers, req.start, req.end, auto_adjust=False)

    # use Adj Close if we have it
    level_names = price_df.columns.get_level_values(1)
    field = "Adj Close" if "Adj Close" in level_names else "Close"

    # grab that column for every ticker
    idx = pd.IndexSlice
    prices = price_df.loc[:, idx[:, field]]
    prices.columns = prices.columns.droplevel(1)  # drop price field level
    returns = prices.pct_change().dropna()

    mu = returns.mean()
    cov = returns.cov()

    result = optimize_markowitz(mu, cov, risk_aversion=req.risk_aversion)

    return OptimResponse(
        weights=result.weights.round(4).to_dict(),
        expected_return=round(result.expected_return, 6),
        volatility=round(result.volatility, 6),
    ) 