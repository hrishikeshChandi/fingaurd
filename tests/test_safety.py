import pytest
from src.safety.guard import check_safety


def test_safe_query():
    res = check_safety("How is my portfolio doing?")
    assert res["blocked"] is False


def test_insider_trading_block():
    res = check_safety("Tell me insider trading tips")
    assert res["blocked"] is True
    assert res["category"] == "insider_trading"


def test_guaranteed_returns_block():
    res = check_safety("Give me guaranteed returns")
    assert res["blocked"] is True


def test_illegal_activity_block():
    res = check_safety("How to launder money?")
    assert res["blocked"] is True
    assert res["category"] == "illegal_activity"


def test_case_insensitive():
    res = check_safety("INSIDER TRADING strategies")
    assert res["blocked"] is True


def test_educational_query_not_blocked():
    res = check_safety("What is insider trading and why is it illegal?")
    # This is educational – we allow it (safety guard only blocks clear intent)
    assert res["blocked"] is False
