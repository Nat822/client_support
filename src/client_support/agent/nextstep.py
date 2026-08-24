from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class AgentContext:
    ticket_id: str
    category: str
    ticket_text: str
    extracted: dict[str, object]


@dataclass(frozen=True, slots=True)
class ToolCall:
    tool_name: str
    arguments: dict[str, object]


@dataclass(frozen=True, slots=True)
class AgentPlan:
    reason: str
    calls: list[ToolCall]
    done: bool = False
    response: str | None = None


@dataclass(frozen=True, slots=True)
class ToolResult:
    tool_name: str
    success: bool
    output: dict[str, object]
    error: str | None = None


class NextStepPlanner(Protocol):
    def next_step(self, context: AgentContext, history: list[ToolResult]) -> AgentPlan: ...


class ToolRuntime(Protocol):
    def execute(self, call: ToolCall) -> ToolResult: ...


@dataclass(frozen=True, slots=True)
class AgentResult:
    status: str
    response: str | None
    steps: int
    history: list[ToolResult]


class NextStepAgent:
    def __init__(self, planner: NextStepPlanner, tools: ToolRuntime, *, max_steps: int = 8) -> None:
        if max_steps < 1:
            raise ValueError("max_steps must be positive")
        self._planner = planner
        self._tools = tools
        self._max_steps = max_steps

    def run(self, context: AgentContext) -> AgentResult:
        history: list[ToolResult] = []
        seen_calls: set[tuple[str, str]] = set()

        for step in range(1, self._max_steps + 1):
            plan = self._planner.next_step(context, history)
            if plan.done:
                return AgentResult("completed", plan.response, step - 1, history)

            if not plan.calls:
                return AgentResult("blocked", None, step - 1, history)

            for call in plan.calls:
                key = (call.tool_name, repr(sorted(call.arguments.items())))
                if key in seen_calls:
                    return AgentResult("blocked_repeated_action", None, step - 1, history)
                seen_calls.add(key)
                history.append(self._tools.execute(call))

        return AgentResult("max_steps_exceeded", None, self._max_steps, history)
