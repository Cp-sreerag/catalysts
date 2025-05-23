# ===================== app/data.py ============================
"""Utility functions for pulling & caching historical data."""
from pathlib import Path
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from .config import CACHE_PATH

START_DATE = "2010-01-01"


def _cache_file(symbol: str) -> Path:
    return CACHE_PATH / f"{symbol}.parquet"


def get_price_history(symbol: str, end: str | None = None) -> pd.DataFrame:
    """Fetch daily OHLCV data. Cache to disk for speed & limited API calls."""
    end = end or datetime.utcnow().date().isoformat()
    cache_f = _cache_file(symbol)

    if cache_f.exists():
        df = pd.read_parquet(cache_f)
        if df.index.max().date() >= pd.to_datetime(end).date() - timedelta(days=1):
            return df  # fresh enough

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=START_DATE, end=end)
    df.to_parquet(cache_f, index=True)
    return df


