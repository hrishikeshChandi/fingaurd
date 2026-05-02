import re
import json
from pathlib import Path
from typing import Dict

_patterns_path = Path(__file__).parent / "patterns.json"
with open(_patterns_path) as f:
    HARMFUL_PATTERNS = json.load(f)

_MESSAGES = {
    "insider_trading": "I can't assist with requests involving non-public or insider information.",
    "guaranteed_returns": "I can't provide or validate guaranteed-return investment advice.",
    "illegal_activity": "I can't assist with illegal financial activities.",
}


def check_safety(query: str) -> Dict:
    q = query.lower()

    for category, patterns in HARMFUL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, q):
                return {
                    "blocked": True,
                    "category": category,
                    "message": _MESSAGES.get(
                        category, "Request blocked for safety reasons."
                    ),
                }

    return {"blocked": False}
