from client_support.agent.nextstep import (
    AgentContext,
    AgentPlan,
    NextStepAgent,
    ToolCall,
    ToolResult,
)


class FakePlanner:
    def __init__(self) -> None:
        self.calls = 0

    def next_step(self, context: AgentContext, history: list[ToolResult]) -> AgentPlan:
        self.calls += 1
        if not history:
            return AgentPlan("lookup order", [ToolCall("lookup_order", {"order_id": "ORD-1"})])
        return AgentPlan("answer ready", [], done=True, response="Your order is in transit.")


class FakeTools:
    def execute(self, call: ToolCall) -> ToolResult:
        return ToolResult(call.tool_name, True, {"status": "in_transit"})


def test_agent_executes_plan_then_completes() -> None:
    agent = NextStepAgent(FakePlanner(), FakeTools())
    result = agent.run(AgentContext("T1", "order_tracking", "Where is ORD-1?", {"order_numbers": ["ORD-1"]}))
    assert result.status == "completed"
    assert result.steps == 1
    assert result.history[0].output["status"] == "in_transit"


class RepeatingPlanner:
    def next_step(self, context: AgentContext, history: list[ToolResult]) -> AgentPlan:
        return AgentPlan("repeat", [ToolCall("lookup_order", {"order_id": "ORD-1"})])


def test_agent_blocks_repeated_action() -> None:
    result = NextStepAgent(RepeatingPlanner(), FakeTools()).run(
        AgentContext("T1", "order_tracking", "Where?", {})
    )
    assert result.status == "blocked_repeated_action"
