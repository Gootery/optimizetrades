"""Streamlit front-end for the optimisation demo."""
from __future__ import annotations

import datetime as dt
from typing import List

import pandas as pd
import plotly.express as px
import streamlit as st

from optimizetrades.data.market_data import get_price_data
from optimizetrades.optimization.qp_markowitz import optimize_markowitz

st.set_page_config(page_title="OptimizeTrades", layout="wide")

st.title("📈 Portfolio Optimisation Demo")

# ------------------ Sidebar Inputs ------------------
with st.sidebar:
    st.header("Universe & Period")
    tickers: List[str] = st.multiselect(
        "Tickers", ["AAPL", "MSFT", "GOOG", "NVDA", "AMZN", "META"], default=["AAPL", "MSFT", "GOOG"]
    )

    start = st.date_input("Start", value=dt.date(2020, 1, 1))
    end = st.date_input("End", value=dt.date.today())

    st.header("Risk Aversion λ")
    risk_aversion = st.slider("Lambda", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

    run_button = st.button("Run Optimisation")

# ------------------ Main Panel ------------------
if run_button and tickers:
    with st.spinner("Fetching data & optimising..."):
        prices = get_price_data(tickers, start, end)[(slice(None), "Adj Close")]
        prices.columns = prices.columns.droplevel(1)
        returns = prices.pct_change().dropna()

        mu = returns.mean()
        cov = returns.cov()
        result = optimize_markowitz(mu, cov, risk_aversion=risk_aversion)

    st.subheader("Optimal Weights")
    st.table(result.weights.sort_values(ascending=False).to_frame("Weight"))

    st.subheader("Portfolio Metrics")
    st.metric("Expected Return", f"{result.expected_return:.2%}")
    st.metric("Volatility", f"{result.volatility:.2%}")

    # Plot price history & cumulative returns
    cum_returns = (1 + returns).cumprod()
    fig_prices = px.line(cum_returns, title="Cumulative Returns")
    st.plotly_chart(fig_prices, use_container_width=True)

else:
    st.info("Select tickers and click *Run Optimisation* to begin.") 