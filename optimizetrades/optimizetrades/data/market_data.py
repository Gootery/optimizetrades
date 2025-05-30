"""Market data acquisition helpers.

Currently relies on yfinance for prototyping. Swap out with your vendor SDK
or internal database calls in production.
"""
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
    """Download historical OHLCV prices for *tickers* between *start* and *end*.

    Parameters
    ----------
    tickers : list[str] | str
        Single ticker or list of tickers (e.g., ["AAPL", "MSFT"]).
    start, end : str | datetime
        Inclusive date range. *end* defaults to today if ``None``.
    interval : str
        Data frequency supported by yfinance ("1d", "1wk", "1mo", etc.).
    auto_adjust : bool, default True
        Whether to back-adjust prices for splits/dividends.

    Returns
    -------
    pandas.DataFrame
        Columns are a MultiIndex (ticker, field) with *field* in
        {"Open", "High", "Low", "Close", "Adj Close", "Volume"}.
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

    # yfinance returns differently-shaped frames for single vs multi-ticker.
    if isinstance(tickers, str):
        # Single ticker → add outer level for consistency
        df.columns = pd.MultiIndex.from_product([[tickers], df.columns])

    # Drop rows with no trading volume across all tickers
    df = df.sort_index().dropna(how="all")
    return df 