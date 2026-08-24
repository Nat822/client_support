from uuid import uuid4

from client_support.application.policy_audit import make_policy_decision_record
from client_support.contracts.policy import PolicyDecisionType


def test_policy_decision_record_is_versioned_and_auditable() -> None:
    record = make_policy_decision_record(
        run_id=uuid4(),
        decision=PolicyDecisionType.HUMAN_REVIEW,
        reason="fuzzy identity requires review",
    )
    assert record.policy_version == "phase0-v1"
    assert record.decision is PolicyDecisionType.HUMAN_REVIEW
    assert record.reason
    assert record.created_at.tzinfo is not None
