from uuid import UUID

from client_support.contracts.order_tracking import OrderTrackingResult
from client_support.domain.states import TicketState, TicketStateMachine
from client_support.subworkflows.order_tracking import execute_order_tracking, extract_order_tracking_request
from client_support.tools.order_lookup import OrderLookupTool


class OrderTrackingApplication:
    """First vertical slice: deterministic routing/extraction/tool execution.

    LLM/NextStep planning is intentionally not embedded here. This runner establishes
    the contract that a future planner must satisfy.
    """

    def __init__(self, lookup_tool: OrderLookupTool) -> None:
        self.lookup_tool = lookup_tool

    def execute(self, *, run_id: UUID, message: str, customer_id: str | None = None) -> OrderTrackingResult:
        machine = TicketStateMachine()
        machine.transition(TicketState.IDENTITY_PENDING)
        machine.transition(TicketState.IDENTITY_RESOLVED)
        machine.transition(TicketState.ELIGIBILITY_CHECKED)
        machine.transition(TicketState.ROUTING_PENDING)
        machine.transition(TicketState.ROUTED)
        machine.transition(TicketState.EXECUTION_PENDING)

        request = extract_order_tracking_request(message, customer_id)
        records = execute_order_tracking(request, self.lookup_tool)

        if not request.order_numbers:
            machine.transition(TicketState.HUMAN_REVIEW)
            return OrderTrackingResult(
                run_id=run_id,
                customer_message="I need an order number to check the delivery status.",
                requires_human_review=True,
                metadata={"reason": "missing_order_number"},
            )

        missing = [number for number in request.order_numbers if number not in {r.order_number for r in records}]
        if missing:
            machine.transition(TicketState.HUMAN_REVIEW)
            return OrderTrackingResult(
                run_id=run_id,
                orders=records,
                customer_message="I could not find every order in the request, so a specialist should review it.",
                requires_human_review=True,
                metadata={"missing_order_numbers": missing},
            )

        machine.transition(TicketState.POLICY_GATE)
        machine.transition(TicketState.COMPLETED)
        message = "; ".join(
            f"Order {record.order_number}: {record.status}"
            + (f", estimated delivery {record.estimated_delivery}" if record.estimated_delivery else "")
            for record in records
        )
        return OrderTrackingResult(run_id=run_id, orders=records, customer_message=message)
