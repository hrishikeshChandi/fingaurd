from pydantic import BaseModel, Field
from typing import Dict, Optional


class IntentOutput(BaseModel):
    intent: str = Field(
        ...,
        description="Intent name, one of: portfolio_health, market_research, investment_strategy, general_query",
    )
    entities: Dict[str, str] = Field(
        default_factory=dict,
        description="Extracted entities like tickers, amounts, etc.",
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score between 0 and 1"
    )
