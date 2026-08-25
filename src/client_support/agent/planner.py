from dataclasses import dataclass
from typing import Protocol

from client_support.agent.nextstep import AgentContext, AgentPlan, ToolResult


class PlannerProvider(Protocol):
    def plan(self, *, context: AgentContext, history: list[ToolResult]) -> AgentPlan: ...


@dataclass(slots=True)
class LLMNextStepPlanner:
    provider: PlannerProvider

    def next_step(self, context: AgentContext, history: list[ToolResult]) -> AgentPlan:
        plan = self.provider.plan(context=context, history=history)
        if plan.done:
            return plan
        if not plan.calls:
            raise ValueError("LLM planner returned a non-terminal plan without tool calls")
        return AgentPlan(reason=plan.reason, calls=list(plan.calls), done=False)
