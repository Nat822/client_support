from enum import StrEnum

from pydantic import BaseModel, Field


class PolicyDecision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    HUMAN_REVIEW = "human_review"


PolicyDecisionType = PolicyDecision


class PolicyContext(BaseModel):
    identity_resolution_method: str | None = None
    identity_confidence: float | None = Field(default=None, ge=0, le=1)
    support_level: str | None = None
    category_automation_level: str | None = None
    proposed_action: str
    has_side_effect: bool = False


class PolicyResult(BaseModel):
    decision: PolicyDecision
    reasons: list[str] = Field(default_factory=list)
