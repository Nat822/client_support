from uuid import uuid4

from client_support.application.order_tracking_runtime import OrderTrackingRuntime
from client_support.contracts.order_tracking import OrderRecord, OrderTrackingRequest
from client_support.policy.engine import PolicyEngine
from client_support.policy.tool_policy import ToolDefinition, ToolRisk
from client_support.tools.order_lookup import OrderLookupTool
from client_support.tools.registry import RegisteredTool, ToolRegistry
from client_support.tools.runtime import ToolRuntime


def runtime(records: dict[str, OrderRecord]) -> OrderTrackingRuntime:
    registry = ToolRegistry()
    registry.register(
        RegisteredTool(
            definition=ToolDefinition(
                name="lookup_order",
                description="Look up an order",
                risk=ToolRisk.READ,
            ),
            handler=lambda _: {},
        )
    )
    return OrderTrackingRuntime(
        ToolRuntime(registry, PolicyEngine()),
        OrderLookupTool(records),
    )


def test_runtime_executes_lookup_through_policy_boundary() -> None:
    result = runtime(
        {"ORD-123456": OrderRecord(order_number="ORD-123456", status="in_transit")}
    ).execute(
        run_id=uuid4(),
        request=OrderTrackingRequest(
            order_numbers=["ORD-123456"], raw_request="Where is it?"
        ),
    )

    assert result.status == "completed"
    assert result.policy_decision.value == "allow"
    assert result.order == {
        "order_number": "ORD-123456",
        "status": "in_transit",
        "carrier": None,
        "tracking_number": None,
        "estimated_delivery": None,
    }


def test_runtime_routes_unknown_order_to_human_review() -> None:
    result = runtime({}).execute(
        run_id=uuid4(),
        request=OrderTrackingRequest(
            order_numbers=["ORD-999999"], raw_request="Where is it?"
        ),
    )

    assert result.status == "human_review"
    assert result.policy_decision.value == "human_review"
    assert result.reason == "order was not found"


def test_runtime_routes_missing_order_to_human_review() -> None:
    result = runtime({}).execute(
        run_id=uuid4(),
        request=OrderTrackingRequest(
            order_numbers=[], raw_request="Where is my package?"
        ),
    )

    assert result.status == "human_review"
    assert result.reason == "order number is missing"
