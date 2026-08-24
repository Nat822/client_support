from client_support.policy.tool_policy import (
    PolicyDecision,
    PolicyEngine,
    ToolDefinition,
    ToolRisk,
)


def test_read_tools_are_allowed() -> None:
    result = PolicyEngine().evaluate(ToolDefinition("lookup_order", ToolRisk.READ, "Read order"))
    assert result.decision is PolicyDecision.ALLOW


def test_writes_are_blocked_by_default() -> None:
    result = PolicyEngine().evaluate(ToolDefinition("update_ticket", ToolRisk.WRITE, "Update ticket"))
    assert result.decision is PolicyDecision.BLOCK


def test_enabled_writes_still_require_review() -> None:
    result = PolicyEngine(allow_writes=True).evaluate(
        ToolDefinition("update_ticket", ToolRisk.WRITE, "Update ticket")
    )
    assert result.decision is PolicyDecision.HUMAN_REVIEW


def test_customer_facing_actions_require_review() -> None:
    result = PolicyEngine().evaluate(
        ToolDefinition("send_reply", ToolRisk.CUSTOMER_FACING, "Send customer reply")
    )
    assert result.decision is PolicyDecision.HUMAN_REVIEW
