import asyncio
import json
import logging
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from src.api.models import QueryRequest, FinalResponse
from src.safety.guard import check_safety
from src.classifier.intent import classify
from src.agents.portfolio_engine import run_portfolio_engine
from src.agents.risk_rules import analyze_risk
from src.memory.session import get_history, add_message, clear_session
from src.metrics.tracker import tracker

logger = logging.getLogger(__name__)
router = APIRouter()

TEST_PORTFOLIO = [
    {"ticker": "AAPL", "quantity": 10},
    {"ticker": "MSFT", "quantity": 5},
]


def _sse_event(event: str, data: dict) -> dict:
    return {"event": event, "data": json.dumps(data, ensure_ascii=False)}


def _portfolio_to_engine_format(portfolio: list) -> list:
    """Convert Pydantic holdings to engine format."""
    if not portfolio:
        return []
    return [{"ticker": h.ticker, "quantity": h.quantity} for h in portfolio]


@router.post("/query")
async def query(req: QueryRequest):
    tracker.record_request()
    start_time = tracker.start_timer()

    async def event_generator():
        final_summary = None
        final_risk_flags = []
        final_metrics = {}

        try:
            safety = check_safety(req.query)
            if safety["blocked"]:
                tracker.record_blocked()
                yield _sse_event(
                    "message",
                    {
                        "stage": "blocked",
                        "reason": safety["category"],
                        "message": safety["message"],
                    },
                )
                yield _sse_event("message", {"stage": "complete", "status": "blocked"})
                tracker.end_timer(start_time)
                return

            yield _sse_event("message", {"stage": "safety_passed"})

            history = get_history(req.session_id)
            if history:
                logger.info(
                    f"Session {req.session_id}: {len(history)} previous messages"
                )

            intent_result = classify(req.query, history)
            tracker.record_intent(intent_result.intent)

            add_message(req.session_id, "user", req.query)

            yield _sse_event(
                "message",
                {
                    "stage": "intent",
                    "intent": intent_result.intent,
                    "entities": intent_result.entities,
                    "confidence": intent_result.confidence,
                    "history_length": len(history),
                },
            )

            if intent_result.intent == "portfolio_health":
                # Use provided portfolio or fallback to test portfolio
                engine_portfolio = (
                    _portfolio_to_engine_format(req.portfolio)
                    if req.portfolio
                    else TEST_PORTFOLIO
                )
                portfolio_metrics = await asyncio.to_thread(
                    run_portfolio_engine, engine_portfolio
                )

                final_metrics = portfolio_metrics

                yield _sse_event(
                    "message", {"stage": "metrics", "metrics": portfolio_metrics}
                )

                risk_analysis = analyze_risk(portfolio_metrics)
                final_risk_flags = risk_analysis.get("risk_flags", [])
                final_summary = risk_analysis.get("summary", "Analysis complete.")

                yield _sse_event(
                    "message", {"stage": "risk_analysis", "risk": risk_analysis}
                )

                add_message(
                    req.session_id,
                    "assistant",
                    f"Risk analysis completed: {final_summary[:100]}",
                )

            # Send final structured response
            final_response = FinalResponse(
                summary=final_summary or "Query processed successfully.",
                risk_flags=final_risk_flags,
                metrics=final_metrics,
            )
            yield _sse_event("result", final_response.model_dump())

            yield _sse_event("message", {"stage": "complete", "status": "success"})

        except Exception as e:
            tracker.record_error()
            logger.error(f"Streaming error: {e}", exc_info=True)
            yield _sse_event("error", {"stage": "error", "message": str(e)})
            yield _sse_event("message", {"stage": "complete", "status": "error"})
        finally:
            tracker.end_timer(start_time)

    return EventSourceResponse(event_generator())


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}


@router.get("/metrics")
async def get_metrics():
    """Return system metrics."""
    return tracker.get_stats()
