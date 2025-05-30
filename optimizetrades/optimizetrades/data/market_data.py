"""Price data helpers (uses yfinance for now)."""
from __future__ import annotations

from datetime import datetime
from typing import List

import pandas as pd
import yfinance as yf


def get_price_data(
    tickers: List[str] | str,
    start: str | datetime,
    end: str | datetime | None = None,
    interval: str = "1d",
    auto_adjust: bool = True,
) -> pd.DataFrame:
    """Grab OHLCV data from yfinance.

    * ``tickers`` can be a list or single str.
    * ``start``/``end`` are the date range (end defaults to today).
    * ``interval`` like "1d", "1wk", etc.
    * If ``auto_adjust`` is True yfinance back-adjusts prices.
    Returns a DataFrame with a (ticker, field) MultiIndex.
    """
    df = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=auto_adjust,
        progress=False,
        threads=True,
        group_by="ticker",
    )

    # if single ticker, slap on an outer level so shape matches multi-ticker
    if isinstance(tickers, str):
        df.columns = pd.MultiIndex.from_product([[tickers], df.columns])

    # drop rows where every ticker has NaNs (market holiday etc.)
    df = df.sort_index().dropna(how="all")
    return df 