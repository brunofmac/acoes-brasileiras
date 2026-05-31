# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Single-file Streamlit dashboard displaying Brazilian B3 stocks (Petrobras, Itaú, Vale) with price, performance, and volume charts. Data is fetched from Yahoo Finance via yfinance.

## Running the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

App runs on `http://localhost:8501` by default.

## Adding or modifying tickers

Stocks are defined in two dicts at the top of `app.py`:

```python
TICKERS = {"Display Name": "TICKER.SA", ...}
CORES  = {"Display Name": "#hexcolor", ...}
```

Yahoo Finance appends `.SA` for B3-listed stocks (e.g. `PETR4.SA`). Both dicts must stay in sync.

## Data caching

`@st.cache_data(ttl=3600)` caches yfinance responses for 1 hour. To force a refresh during development, use `st.cache_data.clear()` or restart the app.

## Python version

Requires Python 3.10+ (uses `list[str]` type hint syntax). No pinned version in requirements.txt.

## UI language

All UI text and comments are in Portuguese.
