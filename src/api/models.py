from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class Holding(BaseModel):
    ticker: str
    quantity: float


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    user_id: str
    session_id: str
    portfolio: Optional[List[Holding]] = None


class FinalResponse(BaseModel):
    summary: str
    risk_flags: List[str]
    metrics: Dict[str, Any]
