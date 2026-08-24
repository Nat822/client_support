from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field

class DomainEvent(BaseModel):
    event_id: str
    run_id: str
    ticket_id: str
    sequence: int = Field(ge=1)
    event_type: str
    payload: dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
