import pytest
from src.agents.portfolio_engine import run_portfolio_engine


def test_empty_portfolio():
    result = run_portfolio_engine([])
    assert result["status"] == "empty"


def test_valid_portfolio():
    portfolio = [{"ticker": "AAPL", "quantity": 10}, {"ticker": "MSFT", "quantity": 5}]
    result = run_portfolio_engine(portfolio)
    assert result["status"] == "ok"
    assert "total_value" in result
    assert "sharpe_ratio" in result
    assert result["total_value"] > 0


def test_concentration_calculation():
    portfolio = [{"ticker": "AAPL", "quantity": 100}, {"ticker": "MSFT", "quantity": 1}]
    result = run_portfolio_engine(portfolio)
    # Apple should dominate
    assert result["concentration"] > 0.9


def test_invalid_ticker():
    portfolio = [{"ticker": "INVALID123", "quantity": 10}]
    result = run_portfolio_engine(portfolio)
    # Should still return "ok" but metrics may be zero/fallback
    assert result["status"] in ["ok", "error"]
