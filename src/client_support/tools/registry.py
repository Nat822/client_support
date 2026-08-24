from collections.abc import Callable
from dataclasses import dataclass

from client_support.agent.nextstep import ToolCall, ToolResult
from client_support.policy.tool_policy import PolicyDecision, PolicyEngine, ToolDefinition


ToolHandler = Callable[[dict[str, object]], dict[str, object]]


@dataclass(frozen=True, slots=True)
class RegisteredTool:
    definition: ToolDefinition
    handler: ToolHandler


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, tool: RegisteredTool) -> None:
        if tool.definition.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.definition.name}")
        self._tools[tool.definition.name] = tool

    def get(self, name: str) -> RegisteredTool | None:
        return self._tools.get(name)

    def names(self) -> list[str]:
        return sorted(self._tools)


class PolicyAwareToolRuntime:
    def __init__(self, registry: ToolRegistry, policy: PolicyEngine) -> None:
        self._registry = registry
        self._policy = policy

    def execute(self, call: ToolCall) -> ToolResult:
        registered = self._registry.get(call.tool_name)
        if registered is None:
            return ToolResult(call.tool_name, False, {}, "unknown tool")

        decision = self._policy.evaluate(registered.definition)
        if decision.decision is not PolicyDecision.ALLOW:
            return ToolResult(call.tool_name, False, {}, decision.reason)

        try:
            return ToolResult(call.tool_name, True, registered.handler(call.arguments))
        except Exception as exc:
            return ToolResult(call.tool_name, False, {}, str(exc))
