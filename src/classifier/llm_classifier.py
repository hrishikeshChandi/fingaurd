# src/classifier/llm_classifier.py
import logging
from langchain.chat_models import init_chat_model
from src.classifier.schema import IntentOutput
from src.config import settings

logger = logging.getLogger(__name__)

# Initialize Groq LLM with structured output
llm = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    temperature=0.0,
    api_key=settings.groq_api_key,
)
structured_llm = llm.with_structured_output(IntentOutput)

SYSTEM_PROMPT = """
You are an intent classifier for a financial advisory system.  
Given the user's query (and optionally the conversation history), output structured JSON with:
- intent: one of ["portfolio_health", "market_research", "investment_strategy", "general_query"]
- entities: a dictionary with keys like "ticker", "amount", "time_period" (extract if present)
- confidence: float between 0 and 1

Do not answer the query, only classify.
"""


def classify_with_llm(query: str, conversation_history: list = None) -> IntentOutput:
    """Classify intent using Groq LLM with structured output."""
    # Prepare messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation history (last 3 turns to keep context)
    if conversation_history:
        for turn in conversation_history[-3:]:
            messages.append({"role": turn["role"], "content": turn["content"]})

    messages.append({"role": "user", "content": query})

    try:
        result = structured_llm.invoke(messages)
        logger.info(
            f"LLM classification: intent={result.intent}, conf={result.confidence}"
        )
        return result
    except Exception as e:
        logger.error(f"LLM classification failed: {e}, falling back to keyword matcher")
        return _fallback_classify(query)


def _fallback_classify(query: str) -> IntentOutput:
    """Fallback keyword matcher (keeps existing behaviour)."""
    query_lower = query.lower()
    if any(
        word in query_lower
        for word in ["portfolio", "holdings", "risk", "diversification"]
    ):
        return IntentOutput(intent="portfolio_health", entities={}, confidence=0.7)
    elif any(word in query_lower for word in ["market", "stock", "sector", "trend"]):
        return IntentOutput(intent="market_research", entities={}, confidence=0.7)
    elif any(
        word in query_lower for word in ["invest", "strategy", "allocate", "rebalance"]
    ):
        return IntentOutput(intent="investment_strategy", entities={}, confidence=0.7)
    else:
        return IntentOutput(intent="general_query", entities={}, confidence=0.6)
