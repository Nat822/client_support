"""Live NeuralDeep planner smoke test. Requires NEURALDEEP_API_KEY."""

import os

from client_support.agent.nextstep import AgentContext
from client_support.providers.neuraldeep_planner import NeuralDeepPlannerProvider


def main() -> None:
    provider = NeuralDeepPlannerProvider.from_environment()
    result = provider.plan(
        context=AgentContext(
            ticket_id="eval-planner-1",
            category="order_tracking",
            ticket_text="Where is my order ORD-123?",
            extracted={"order_id": "ORD-123"},
        ),
        history=[],
    )
    print({"model": provider.model, "done": result.done, "reason": result.reason, "calls": [c.tool_name for c in result.calls]})
    if result.done or not result.calls:
        raise SystemExit("NeuralDeep planner did not produce an executable tool plan")


if __name__ == "__main__":
    if not os.environ.get("NEURALDEEP_API_KEY"):
        raise SystemExit("NEURALDEEP_API_KEY is required")
    main()
