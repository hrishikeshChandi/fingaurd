# src/agents/risk_rules.py
from src.adaptive_thresholds import adaptive


def analyze_risk(metrics: dict):
    if metrics.get("status") != "ok":
        return {"risk_flags": [], "summary": "No analysis available"}

    # Record metrics for adaptive learning
    adaptive.record_metrics(
        concentration=metrics.get("concentration", 0),
        sharpe=metrics.get("sharpe_ratio", 0),
        drawdown=metrics.get("max_drawdown", 0),
        volatility=metrics.get("volatility", 0),
    )

    # Get dynamic thresholds (learned from historical data)
    thresholds = adaptive.get_thresholds()

    flags = []
    concentration = metrics.get("concentration", 0)
    sharpe = metrics.get("sharpe_ratio", 0)
    drawdown = metrics.get("max_drawdown", 0)
    volatility = metrics.get("volatility", 0)

    if concentration > thresholds["concentration_threshold"]:
        flags.append(
            f"⚠️ High concentration risk ({concentration*100:.0f}% in single asset)"
        )

    if sharpe < thresholds["sharpe_threshold"]:
        flags.append(f"⚠️ Poor risk-adjusted returns (Sharpe: {sharpe:.2f})")

    if drawdown < thresholds["drawdown_threshold"]:
        flags.append(f"⚠️ High historical drawdown ({drawdown*100:.0f}% loss)")

    if volatility > thresholds["volatility_threshold"]:
        flags.append(f"⚠️ High volatility ({volatility*100:.0f}%)")

    summary = (
        "Portfolio appears reasonably balanced."
        if not flags
        else "Portfolio shows risk signals: " + "; ".join(flags)
    )
    return {"risk_flags": flags, "summary": summary}
