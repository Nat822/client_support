"""Live end-to-end NeuralDeep planner + policy + fake read tool smoke test."""

import os

from client_support.agent.nextstep import AgentContext, ToolResult
from client_support.agent.planner import LLMNextStepPlanner
from client_support.agent.runtime import AgentRuntime, PolicyAwareToolRuntime, RegisteredTool
from client_support.policy.tool_policy import PolicyEngine, ToolDefinition, ToolRisk
from client_support.providers.neuraldeep_planner import NeuralDeepPlannerProvider


def lookup_order(arguments: dict[str, object]) -> dict[str, object]:
    return {"order_id": arguments.get("order_id", "ORD-123"), "status": "in_transit"}


class FixedProvider:
    """Only the tool observation is deterministic; planning remains live NeuralDeep."""
    def __init__(self, provider: NeuralDeepPlannerProvider) -> None:
        self.provider = provider

    def plan(self, *, context, history: list[ToolResult]):
        return self.provider.plan(context=context, history=history)


def main() -> None:
    provider = NeuralDeepPlannerProvider.from_environment()
    planner = LLMNextStepPlanner(FixedProvider(provider))
    runtime = PolicyAwareToolRuntime(
        {"lookup_order": RegisteredTool(ToolDefinition("lookup_order", ToolRisk.READ, "Read order status"), lookup_order)},
        PolicyEngine(),
    )
    result = AgentRuntime(planner, runtime, max_steps=4).run(
        AgentContext("e2e-1", "order_tracking", "Where is order ORD-123?", {"order_id": "ORD-123"})
    )
    print({"status": result.status, "steps": result.steps, "history": [r.output for r in result.history]})
    if result.status != "completed":
        raise SystemExit(f"E2E agent did not complete: {result.status}")


if __name__ == "__main__":
    if not os.environ.get("NEURALDEEP_API_KEY"):
        raise SystemExit("NEURALDEEP_API_KEY is required")
    main()
