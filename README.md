Portfolio Optimization Tool – Markowitz, Black-Litterman, Factor-Model
This repository contains a research-friendly yet production-ready Python stack for portfolio optimisation with support for:

Mean–variance optimisation (Markowitz) using convex quadratic programming
Black-Litterman Bayesian blending of market equilibrium and subjective views
Factor-model risk (fundamental or statistical)
Rich, reusable constraint library (sector caps, turnover, leverage, ESG, etc.)
Efficient-frontier visualisation via Streamlit or REST + React
Quick-start (Streamlit)
# Create a virtual environment & install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Launch the demo UI
streamlit run optimizetrades/app/streamlit_app.py
Quick-start (API)
uvicorn optimizetrades.api.main:app --reload
Project layout
optimizetrades/
│   __init__.py
│
├── data/            # data connectors & caching
├── core/            # return & risk models
├── constraints/     # constraint objects
├── optimization/    # cvxpy models & solvers
├── api/             # FastAPI layer
├── app/             # Streamlit Front-end (or swap for React)
└── tests/           # pytest suite
For the full roadmap, see docs/outline.md (coming soon).
