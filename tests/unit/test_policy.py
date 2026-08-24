from client_support.contracts.policy import PolicyContext, PolicyDecision
from client_support.policy.engine import PolicyEngine

def test_fuzzy_identity_requires_review():
    result = PolicyEngine().evaluate(PolicyContext(
        identity_resolution_method="fuzzy",
        identity_confidence=0.91,
        category_automation_level="full",
        proposed_action="draft_email",
    ))
    assert result.decision == PolicyDecision.HUMAN_REVIEW
    assert "identity_resolved_by_fuzzy_match" in result.reasons

def test_fully_automated_read_only_path_is_allowed():
    result = PolicyEngine().evaluate(PolicyContext(
        identity_resolution_method="exact_email",
        identity_confidence=1.0,
        category_automation_level="full",
        proposed_action="draft_email",
    ))
    assert result.decision == PolicyDecision.ALLOW
