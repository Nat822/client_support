from dataclasses import dataclass

from client_support.agent.nextstep import AgentContext, AgentResult, NextStepAgent
from client_support.agent.planner import LLMNextStepPlanner
from client_support.policy.tool_policy import PolicyDecision, PolicyEngine, ToolDefinition
from client_support.agent.nextstep import ToolCall, ToolResult


@dataclass(slots=True)
class RegisteredTool:
    definition: ToolDefinition
    handler: object


class PolicyAwareToolRuntime:
    def __init__(self, registry: dict[str, RegisteredTool], policy: PolicyEngine) -> None:
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
            output = registered.handler(call.arguments)
        except Exception as exc:  # noqa: BLE001
            return ToolResult(call.tool_name, False, {}, f"tool execution failed: {exc}")
        return ToolResult(call.tool_name, True, output)


class AgentRuntime:
    def __init__(self, planner: LLMNextStepPlanner, tools: PolicyAwareToolRuntime, *, max_steps: int = 8) -> None:
        self._agent = NextStepAgent(planner, tools, max_steps=max_steps)

    def run(self, context: AgentContext) -> AgentResult:
        return self._agent.run(context)
