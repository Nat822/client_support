from uuid import UUID, uuid4

from client_support.contracts.identity import CustomerRef, IdentityResolutionMethod
from client_support.domain.run import ExecutionRun, RunStatus
from client_support.domain.states import TicketState
from client_support.domain.ticket import Ticket
from client_support.policy.engine import PolicyEngine
from client_support.repositories.in_memory import (
    InMemoryEventRepository,
    InMemoryRunRepository,
    InMemoryTicketRepository,
)
from client_support.telemetry import EventRecorder


class Phase0Execution:
    """Deterministic foundation runner used before real integrations/LLM execution."""

    def __init__(
        self,
        tickets: InMemoryTicketRepository | None = None,
        runs: InMemoryRunRepository | None = None,
        events: InMemoryEventRepository | None = None,
    ) -> None:
        self.tickets = tickets or InMemoryTicketRepository()
        self.runs = runs or InMemoryRunRepository()
        self.events = events or InMemoryEventRepository()
        self.policy = PolicyEngine()

    def run(
        self,
        *,
        subject: str,
        requester_email: str,
        identity_method: IdentityResolutionMethod = IdentityResolutionMethod.EXACT_EMAIL,
    ) -> ExecutionRun:
        ticket = Ticket(id=uuid4(), subject=subject, requester_email=requester_email)
        run = ExecutionRun(id=uuid4(), ticket_id=ticket.id)
        self.tickets.add(ticket)
        self.runs.add(run)
        recorder = EventRecorder(self.events.append)

        def transition(state: TicketState, event_type: str) -> None:
            ticket.state = state
            run.sequence += 1
            recorder.record(
                run_id=run.id,
                ticket_id=ticket.id,
                sequence=run.sequence,
                event_type=event_type,
                payload={"state": state.value},
            )

        transition(TicketState.IDENTITY_PENDING, "identity.pending")
        ticket.customer = CustomerRef(
            customer_id="SYNTH-CUSTOMER-001",
            method=identity_method,
            confidence=0.99 if identity_method is IdentityResolutionMethod.EXACT_EMAIL else 0.78,
            matched_fields=["email"] if identity_method is IdentityResolutionMethod.EXACT_EMAIL else ["domain", "name"],
        )
        transition(TicketState.IDENTITY_RESOLVED, "identity.resolved")
        transition(TicketState.ELIGIBILITY_CHECKED, "ticket.eligibility_checked")
        transition(TicketState.ROUTING_PENDING, "routing.pending")
        ticket.category = "order_tracking"
        ticket.support_level = "full"
        transition(TicketState.ROUTED, "ticket.routed")
        transition(TicketState.EXECUTION_PENDING, "execution.pending")
        decision = self.policy.evaluate(customer=ticket.customer, category_support="full")
        run.metadata["policy_decision"] = decision.decision.value
        run.metadata["policy_reason"] = decision.reason
        run.sequence += 1
        recorder.record(
            run_id=run.id,
            ticket_id=ticket.id,
            sequence=run.sequence,
            event_type="policy.evaluated",
            payload={"decision": decision.decision.value, "reason": decision.reason},
        )
        if decision.decision.value == "human_review":
            run.status = RunStatus.HUMAN_REVIEW
            ticket.state = TicketState.HUMAN_REVIEW
            return run

        transition(TicketState.POLICY_GATE, "policy.approved")
        run.status = RunStatus.COMPLETED
        transition(TicketState.COMPLETED, "run.completed")
        return run
