# src/adaptive_thresholds.py
import json
import os
from statistics import mean, stdev

THRESHOLD_HISTORY_FILE = "threshold_history.json"


class AdaptiveThresholds:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(THRESHOLD_HISTORY_FILE):
            with open(THRESHOLD_HISTORY_FILE, "r") as f:
                return json.load(f)
        return {"concentration": [], "sharpe": [], "drawdown": [], "volatility": []}

    def _save_history(self):
        with open(THRESHOLD_HISTORY_FILE, "w") as f:
            json.dump(self.history, f, indent=2)

    def record_metrics(self, concentration, sharpe, drawdown, volatility):
        """Append new metrics, keep window size."""
        self.history["concentration"].append(concentration)
        self.history["sharpe"].append(sharpe)
        self.history["drawdown"].append(drawdown)
        self.history["volatility"].append(volatility)

        for key in self.history:
            if len(self.history[key]) > self.window_size:
                self.history[key] = self.history[key][-self.window_size :]

        self._save_history()

    def get_thresholds(self):
        """Return dynamic thresholds based on percentiles."""

        def percentile(data, p):
            if not data:
                return None
            sorted_data = sorted(data)
            idx = int(len(sorted_data) * p)
            return sorted_data[min(idx, len(sorted_data) - 1)]

        return {
            "concentration_threshold": percentile(self.history["concentration"], 0.80)
            or 0.5,
            "sharpe_threshold": percentile(self.history["sharpe"], 0.20) or 1.0,
            "drawdown_threshold": percentile(self.history["drawdown"], 0.20) or -0.3,
            "volatility_threshold": percentile(self.history["volatility"], 0.80) or 0.3,
        }


adaptive = AdaptiveThresholds()
