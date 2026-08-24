from uuid import uuid4

from client_support.application.order_tracking_runtime import OrderTrackingRuntime
from client_support.contracts.policy import PolicyDecisionType
from client_support.policy.engine import PolicyEngine
from client_support.subworkflows.order_tracking import OrderTrackingRequest
from client_support.tools.order_lookup import OrderLookupTool
from client_support.tools.registry import ToolDefinition, ToolRegistry
from client_support.tools.runtime import ToolRuntime


def make_runtime() -> OrderTrackingRuntime:
    registry = ToolRegistry()
    registry.register(ToolDefinition(name="lookup_order", description="Look up an order"))
    return OrderTrackingRuntime(
        ToolRuntime(registry, PolicyEngine()),
        OrderLookupTool(),
    )


def test_order_tracking_uses_phase0_tool_safety_boundary() -> None:
    result = make_runtime().execute(
        run_id=uuid4(),
        request=OrderTrackingRequest(message="Where is order ORD-001?"),
    )
    assert result.status == "completed"
    assert result.policy_decision is PolicyDecisionType.ALLOW
    assert result.order is not None


def test_order_tracking_sends_missing_order_to_review() -> None:
    result = make_runtime().execute(
        run_id=uuid4(),
        request=OrderTrackingRequest(message="Where is my package?"),
    )
    assert result.status == "human_review"
    assert result.policy_decision is PolicyDecisionType.HUMAN_REVIEW
