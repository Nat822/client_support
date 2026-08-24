from uuid import uuid4

from client_support.contracts.policy import PolicyContext
from client_support.policy.engine import PolicyEngine
from client_support.policy.tool_policy import ToolDefinition, ToolRisk
from client_support.tools.registry import RegisteredTool, ToolRegistry
from client_support.tools.runtime import ToolRuntime


def test_tool_runtime_blocks_before_handler_for_fuzzy_identity() -> None:
    registry = ToolRegistry()
    registry.register(
        RegisteredTool(
            definition=ToolDefinition(
                name="send_reply",
                description="Send customer reply",
                risk=ToolRisk.CUSTOMER_FACING,
            ),
            handler=lambda _: {"sent": True},
        )
    )
    runtime = ToolRuntime(registry, PolicyEngine())
    called = False

    def handler(_: dict[str, object]) -> dict[str, object]:
        nonlocal called
        called = True
        return {"sent": True}

    execution = runtime.execute(
        run_id=uuid4(),
        tool_name="send_reply",
        arguments={"body": "hello"},
        policy_context=PolicyContext(
            identity_resolution_method="fuzzy",
            identity_confidence=0.78,
            category_automation_level="full",
            proposed_action="send_reply",
        ),
        handler=handler,
    )

    assert execution.result.status == "blocked"
    assert called is False


def test_tool_runtime_executes_only_after_policy_allows() -> None:
    registry = ToolRegistry()
    registry.register(
        RegisteredTool(
            definition=ToolDefinition(
                name="lookup_order",
                description="Look up an order",
                risk=ToolRisk.READ,
            ),
            handler=lambda args: {"order_id": args["order_id"]},
        )
    )
    runtime = ToolRuntime(registry, PolicyEngine())

    execution = runtime.execute(
        run_id=uuid4(),
        tool_name="lookup_order",
        arguments={"order_id": "ORD-001"},
        policy_context=PolicyContext(
            identity_resolution_method="exact_email",
            identity_confidence=1.0,
            category_automation_level="full",
            proposed_action="lookup_order",
        ),
        handler=lambda args: {"order_id": args["order_id"], "status": "in_transit"},
    )

    assert execution.result.status == "completed"
    assert execution.result.data["status"] == "in_transit"
