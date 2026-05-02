import numpy as np
import pandas as pd
import yfinance as yf
from typing import List, Dict


def fetch_price_data(tickers: List[str], period: str = "1y") -> pd.DataFrame:
    data = yf.download(tickers, period=period)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()
    return data.dropna()


def compute_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    return price_df.pct_change().dropna()


def compute_portfolio_value(portfolio: List[Dict], latest_prices: pd.Series) -> tuple:
    total = 0.0
    values = {}
    for holding in portfolio:
        ticker = holding["ticker"]
        qty = holding["quantity"]
        value = qty * latest_prices[ticker]
        values[ticker] = value
        total += value
    return total, values


def compute_concentration(values: Dict) -> float:
    if not values:
        return 0.0
    total = sum(values.values())
    if total == 0:
        return 0.0
    return max(values.values()) / total


def compute_volatility(returns: pd.DataFrame) -> float:
    return float(returns.std().mean() * np.sqrt(252))


def compute_sharpe(returns: pd.DataFrame, risk_free_rate: float = 0.02) -> float:
    mean_return = returns.mean().mean() * 252
    vol = compute_volatility(returns)
    if vol == 0:
        return 0.0
    return (mean_return - risk_free_rate) / vol


def compute_max_drawdown(price_df: pd.DataFrame) -> float:
    cumulative = (1 + price_df.pct_change()).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return float(drawdown.min().min())


def run_portfolio_engine(portfolio: List[Dict]) -> Dict:
    if not portfolio:
        return {"status": "empty", "message": "Portfolio is empty"}

    tickers = [p["ticker"] for p in portfolio]

    try:
        prices = fetch_price_data(tickers)
        latest_prices = prices.iloc[-1]
        returns = compute_returns(prices)
        total_value, values = compute_portfolio_value(portfolio, latest_prices)

        return {
            "status": "ok",
            "total_value": round(float(total_value), 2),
            "concentration": round(compute_concentration(values), 4),
            "volatility": round(compute_volatility(returns), 4),
            "sharpe_ratio": round(compute_sharpe(returns), 4),
            "max_drawdown": round(compute_max_drawdown(prices), 4),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
