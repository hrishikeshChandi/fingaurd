from src.agents.risk_rules import analyze_risk
from src.config import settings


def test_high_risk():
    metrics = {
        "status": "ok",
        "concentration": 0.8,
        "sharpe_ratio": 0.5,
        "max_drawdown": -0.4,
        "volatility": 0.4,
    }
    result = analyze_risk(metrics)
    assert len(result["risk_flags"]) > 0
    assert "⚠️ High concentration risk" in result["risk_flags"][0]


def test_low_risk():
    metrics = {
        "status": "ok",
        "concentration": 0.2,
        "sharpe_ratio": 1.5,
        "max_drawdown": -0.1,
        "volatility": 0.1,
    }
    result = analyze_risk(metrics)
    assert result["risk_flags"] == []


def test_threshold_from_settings():
    # Temporarily override settings to test configurable thresholds
    original = settings.concentration_threshold
    settings.concentration_threshold = 0.3
    metrics = {
        "status": "ok",
        "concentration": 0.4,
        "sharpe_ratio": 2,
        "max_drawdown": -0.05,
        "volatility": 0.1,
    }
    result = analyze_risk(metrics)
    assert any("concentration" in f for f in result["risk_flags"])
    settings.concentration_threshold = original
