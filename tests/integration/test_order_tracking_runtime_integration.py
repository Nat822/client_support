from uuid import uuid4

from client_support.application.order_tracking_runtime import OrderTrackingRuntime
from client_support.contracts.order_tracking import OrderRecord, OrderTrackingRequest
from client_support.policy.engine import PolicyEngine
from client_support.tools.order_lookup import OrderLookupTool
from client_support.tools.registry import ToolDefinition, ToolRegistry
from client_support.tools.runtime import ToolRuntime


def make_runtime() -> OrderTrackingRuntime:
    registry = ToolRegistry()
    registry.register(ToolDefinition(name="lookup_order", description="Look up an order"))
    records = {"ORD-001": OrderRecord(order_number="ORD-001", status="in_transit")}
    return OrderTrackingRuntime(
        ToolRuntime(registry, PolicyEngine()),
        OrderLookupTool(records),
    )


def test_order_tracking_uses_phase0_tool_safety_boundary() -> None:
    result = make_runtime().execute(
        run_id=uuid4(),
        request=OrderTrackingRequest(
            order_numbers=["ORD-001"], raw_request="Where is my order?"
        ),
    )
    assert result.status == "completed"
    assert result.policy_decision.value == "allow"
    assert result.order is not None


def test_order_tracking_sends_missing_order_to_review() -> None:
    result = make_runtime().execute(
        run_id=uuid4(),
        request=OrderTrackingRequest(
            order_numbers=[], raw_request="Where is my package?"
        ),
    )
    assert result.status == "human_review"
    assert result.policy_decision.value == "human_review"
