from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from client_support.contracts.policy import PolicyDecisionType


@dataclass(frozen=True, slots=True)
class PolicyDecisionRecord:
    id: UUID
    run_id: UUID
    decision: PolicyDecisionType
    reason: str
    policy_version: str
    created_at: datetime


def make_policy_decision_record(
    *, run_id: UUID, decision: PolicyDecisionType, reason: str, policy_version: str = "phase0-v1"
) -> PolicyDecisionRecord:
    return PolicyDecisionRecord(
        id=uuid4(),
        run_id=run_id,
        decision=decision,
        reason=reason,
        policy_version=policy_version,
        created_at=datetime.now(timezone.utc),
    )
