from dataclasses import dataclass
from typing import Any
from uuid import UUID

from client_support.contracts.order_tracking import OrderTrackingRequest
from client_support.contracts.policy import PolicyContext, PolicyDecisionType
from client_support.tools.order_lookup import OrderLookupTool
from client_support.tools.runtime import ToolRuntime


@dataclass(frozen=True, slots=True)
class OrderTrackingRuntimeResult:
    status: str
    order: dict[str, Any] | None
    policy_decision: PolicyDecisionType
    reason: str


class OrderTrackingRuntime:
    """Run order tracking through the Phase 0 policy and tool boundary."""

    def __init__(self, tool_runtime: ToolRuntime, lookup_tool: OrderLookupTool) -> None:
        self.tool_runtime = tool_runtime
        self.lookup_tool = lookup_tool

    def execute(
        self, *, run_id: UUID, request: OrderTrackingRequest
    ) -> OrderTrackingRuntimeResult:
        if len(request.order_numbers) != 1:
            return OrderTrackingRuntimeResult(
                status="human_review",
                order=None,
                policy_decision=PolicyDecisionType.HUMAN_REVIEW,
                reason=(
                    "order number is missing"
                    if not request.order_numbers
                    else "multiple order numbers require review"
                ),
            )

        order_number = request.order_numbers[0]

        def handler(arguments: dict[str, Any]) -> dict[str, Any]:
            record = self.lookup_tool.execute(str(arguments["order_number"]))
            return {"found": record is not None, "record": record.model_dump() if record else None}

        tool_execution = self.tool_runtime.execute(
            run_id=run_id,
            tool_name="lookup_order",
            arguments={"order_number": order_number},
            policy_context=PolicyContext(
                identity_resolution_method="exact_email",
                identity_confidence=1.0,
                category_automation_level="full",
                proposed_action="lookup_order",
            ),
            handler=handler,
        )
        if tool_execution.result.status != "completed":
            return OrderTrackingRuntimeResult(
                status="human_review",
                order=None,
                policy_decision=PolicyDecisionType.HUMAN_REVIEW,
                reason="tool execution was blocked by policy",
            )

        data = tool_execution.result.data
        if not data.get("found"):
            return OrderTrackingRuntimeResult(
                status="human_review",
                order=None,
                policy_decision=PolicyDecisionType.HUMAN_REVIEW,
                reason="order was not found",
            )

        return OrderTrackingRuntimeResult(
            status="completed",
            order=data["record"],
            policy_decision=PolicyDecisionType.ALLOW,
            reason="order lookup completed",
        )
