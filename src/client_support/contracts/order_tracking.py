from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OrderTrackingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_numbers: list[str] = Field(default_factory=list)
    customer_id: str | None = None
    raw_request: str


class OrderRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order_number: str
    status: str
    carrier: str | None = None
    tracking_number: str | None = None
    estimated_delivery: str | None = None


class OrderTrackingResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: UUID
    category: str = "order_tracking"
    orders: list[OrderRecord] = Field(default_factory=list)
    customer_message: str
    requires_human_review: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)
