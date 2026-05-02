import pytest
from src.classifier.intent import classify, IntentOutput


def test_intent_classifier_portfolio():
    result = classify("How is my portfolio risk?")
    assert result.intent == "portfolio_health"
    assert result.confidence > 0.7


def test_intent_classifier_market():
    result = classify("What are the latest market trends?")
    assert result.intent == "market_research"


def test_intent_classifier_investment():
    result = classify("What's a good investment strategy?")
    assert result.intent == "investment_strategy"


def test_intent_classifier_general():
    result = classify("Hello, how are you?")
    assert result.intent == "general_query"


def test_fallback_on_empty_query():
    result = classify("")
    assert result.intent == "general_query"
    assert result.confidence >= 0.5  # Accept 0.5 or higher
