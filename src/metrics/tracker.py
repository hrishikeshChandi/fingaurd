import time
from typing import List, Dict


class MetricsTracker:
    def __init__(self):
        self.total_requests = 0
        self.errors = 0
        self.latencies: List[float] = []
        self.blocked_requests = 0
        self.intents: Dict[str, int] = {}
        self.start_time = time.time()

    def start_timer(self) -> float:
        return time.time()

    def end_timer(self, start_time: float) -> float:
        latency = time.time() - start_time
        self.latencies.append(latency)
        return latency

    def record_request(self) -> None:
        self.total_requests += 1

    def record_error(self) -> None:
        self.errors += 1

    def record_blocked(self) -> None:
        self.blocked_requests += 1

    def record_intent(self, intent: str) -> None:
        self.intents[intent] = self.intents.get(intent, 0) + 1

    def get_stats(self) -> Dict:
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0
        p95_latency = self._percentile(95) if self.latencies else 0
        uptime = time.time() - self.start_time

        return {
            "total_requests": self.total_requests,
            "blocked_requests": self.blocked_requests,
            "errors": self.errors,
            "success_rate": round(
                (self.total_requests - self.errors - self.blocked_requests)
                / max(self.total_requests, 1)
                * 100,
                2,
            ),
            "avg_latency_seconds": round(avg_latency, 3),
            "p95_latency_seconds": round(p95_latency, 3),
            "intent_distribution": self.intents,
            "uptime_seconds": round(uptime, 0),
        }

    def _percentile(self, p: int) -> float:
        sorted_latencies = sorted(self.latencies)
        idx = int(len(sorted_latencies) * p / 100)
        return sorted_latencies[min(idx, len(sorted_latencies) - 1)]


tracker = MetricsTracker()
