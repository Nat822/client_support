from dataclasses import dataclass
from enum import StrEnum


class ToolRisk(StrEnum):
    READ = "read"
    WRITE = "write"
    CUSTOMER_FACING = "customer_facing"


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    name: str
    risk: ToolRisk
    description: str


class PolicyDecision(StrEnum):
    ALLOW = "allow"
    HUMAN_REVIEW = "human_review"
    BLOCK = "block"


@dataclass(frozen=True, slots=True)
class PolicyResult:
    decision: PolicyDecision
    reason: str


class PolicyEngine:
    def __init__(self, *, allow_writes: bool = False) -> None:
        self._allow_writes = allow_writes

    def evaluate(self, tool: ToolDefinition) -> PolicyResult:
        if tool.risk is ToolRisk.READ:
            return PolicyResult(PolicyDecision.ALLOW, "read-only tool")
        if tool.risk is ToolRisk.WRITE:
            if self._allow_writes:
                return PolicyResult(PolicyDecision.HUMAN_REVIEW, "write requires review")
            return PolicyResult(PolicyDecision.BLOCK, "writes are disabled")
        return PolicyResult(PolicyDecision.HUMAN_REVIEW, "customer-facing action requires human review")
