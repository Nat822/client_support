from dataclasses import dataclass
from typing import Any, Protocol
from uuid import UUID, uuid4

from client_support.contracts.policy import PolicyContext, PolicyDecisionType
from client_support.contracts.tool import ToolCall, ToolResult
from client_support.policy.engine import PolicyEngine
from client_support.tools.registry import ToolRegistry


class ToolHandler(Protocol):
    def __call__(self, arguments: dict[str, Any]) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class ToolExecution:
    call: ToolCall
    result: ToolResult


class ToolRuntime:
    """The only execution boundary for side-effecting tools."""

    def __init__(self, registry: ToolRegistry, policy: PolicyEngine) -> None:
        self.registry = registry
        self.policy = policy

    def execute(
        self,
        *,
        run_id: UUID,
        tool_name: str,
        arguments: dict[str, Any],
        policy_context: PolicyContext,
        handler: ToolHandler,
    ) -> ToolExecution:
        tool = self.registry.get(tool_name)
        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")

        call = ToolCall(id=uuid4(), run_id=run_id, tool_name=tool_name, arguments=arguments)
        decision = self.policy.evaluate(policy_context)
        if decision.decision is not PolicyDecisionType.ALLOW:
            return ToolExecution(
                call=call,
                result=ToolResult(
                    call_id=call.id,
                    status="blocked",
                    data={"reasons": decision.reasons},
                ),
            )

        data = handler(arguments)
        return ToolExecution(
            call=call,
            result=ToolResult(call_id=call.id, status="completed", data=data),
        )
