# tests/conftest.py
import pytest
from unittest.mock import patch
from src.classifier.schema import IntentOutput  # ← ADD THIS


@pytest.fixture(autouse=True)
def mock_llm_classifier():
    with patch("src.classifier.llm_classifier.structured_llm") as mock:
        mock.invoke.return_value = IntentOutput(
            intent="general_query", entities={}, confidence=0.9
        )
        yield
