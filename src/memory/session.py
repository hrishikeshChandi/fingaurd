from collections import defaultdict
from typing import List, Dict

# session_id → list of messages
_sessions: Dict[str, List[Dict]] = defaultdict(list)

MAX_HISTORY = 5


def get_history(session_id: str) -> List[Dict]:
    """Get conversation history for a session (last MAX_HISTORY messages)."""
    return _sessions[session_id][-MAX_HISTORY:]


def add_message(session_id: str, role: str, content: str) -> None:
    """Add a message to session history."""
    _sessions[session_id].append({"role": role, "content": content})


def clear_session(session_id: str) -> None:
    """Clear all history for a session."""
    if session_id in _sessions:
        del _sessions[session_id]
