# src/classifier/intent.py
import logging
from src.classifier.llm_classifier import classify_with_llm
from src.classifier.schema import IntentOutput

logger = logging.getLogger(__name__)


def classify(query: str, conversation_history: list = None) -> IntentOutput:
    """Public entry point – uses LLM, falls back to keyword matcher."""
    return classify_with_llm(query, conversation_history)
