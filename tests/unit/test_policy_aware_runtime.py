from client_support.agent.nextstep import ToolCall
from client_support.policy.tool_policy import PolicyEngine, ToolDefinition, ToolRisk
from client_support.tools.registry import PolicyAwareToolRuntime, RegisteredTool, ToolRegistry


def test_runtime_allows_read_tool() -> None:
    registry = ToolRegistry()
    registry.register(RegisteredTool(
        ToolDefinition("lookup_order", ToolRisk.READ, "Read order"),
        lambda args: {"status": "in_transit", "order_id": args["order_id"]},
    ))
    result = PolicyAwareToolRuntime(registry, PolicyEngine()).execute(
        ToolCall("lookup_order", {"order_id": "ORD-1"})
    )
    assert result.success is True
    assert result.output["status"] == "in_transit"


def test_runtime_blocks_customer_facing_tool() -> None:
    registry = ToolRegistry()
    registry.register(RegisteredTool(
        ToolDefinition("send_reply", ToolRisk.CUSTOMER_FACING, "Send reply"),
        lambda args: {"sent": True},
    ))
    result = PolicyAwareToolRuntime(registry, PolicyEngine()).execute(
        ToolCall("send_reply", {"body": "Hello"})
    )
    assert result.success is False
    assert "human review" in (result.error or "")


def test_runtime_returns_unknown_tool_observation() -> None:
    result = PolicyAwareToolRuntime(ToolRegistry(), PolicyEngine()).execute(
        ToolCall("missing", {})
    )
    assert result.success is False
    assert result.error == "unknown tool"
