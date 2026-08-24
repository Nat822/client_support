from dataclasses import dataclass
from typing import Any
from uuid import UUID

from client_support.contracts.policy import PolicyContext, PolicyDecisionType
from client_support.subworkflows.order_tracking import OrderTrackingRequest, OrderTrackingResult
from client_support.tools.order_lookup import OrderLookupTool
from client_support.tools.registry import ToolRegistry
from client_support.tools.runtime import ToolRuntime
from client_support.policy.engine import PolicyEngine


@dataclass(frozen=True, slots=True)
class OrderTrackingRuntimeResult:
    status: str
    order: dict[str, Any] | None
    policy_decision: PolicyDecisionType
    reason: str


class OrderTrackingRuntime:
    """Runs the order-tracking vertical slice through the Phase 0 safety boundary."""

    def __init__(self, tool_runtime: ToolRuntime, lookup_tool: OrderLookupTool) -> None:
        self.tool_runtime = tool_runtime
        self.lookup_tool = lookup_tool

    def execute(self, *, run_id: UUID, request: OrderTrackingRequest) -> OrderTrackingRuntimeResult:
        result: OrderTrackingResult = request.extract()
        if not result.order_number:
            return OrderTrackingRuntimeResult(
                status="human_review",
                order=None,
                policy_decision=PolicyDecisionType.HUMAN_REVIEW,
                reason="order number could not be extracted",
            )

        tool_execution = self.tool_runtime.execute(
            run_id=run_id,
            tool_name="lookup_order",
            arguments={"order_number": result.order_number},
            policy_context=PolicyContext(
                identity_resolution_method="exact_email",
                identity_confidence=1.0,
                category_automation_level="full",
                proposed_action="lookup_order",
            ),
            handler=self.lookup_tool.execute,
        )
        if tool_execution.result.status != "completed":
            return OrderTrackingRuntimeResult(
                status="human_review",
                order=None,
                policy_decision=PolicyDecisionType.HUMAN_REVIEW,
                reason="tool execution was blocked by policy",
            )

        return OrderTrackingRuntimeResult(
            status="completed",
            order=tool_execution.result.data,
            policy_decision=PolicyDecisionType.ALLOW,
            reason="order lookup completed",
        )
