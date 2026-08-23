from enum import StrEnum

from pydantic import BaseModel, Field


class IdentityResolutionMethod(StrEnum):
    EXACT_EMAIL = "exact_email"
    FUZZY = "fuzzy"
    UNRESOLVED = "unresolved"


class CustomerRef(BaseModel):
    customer_id: str
    method: IdentityResolutionMethod
    confidence: float = Field(ge=0, le=1)
    matched_fields: list[str] = Field(default_factory=list)
