from client_support.contracts.policy import PolicyContext
from client_support.domain.states import TicketState, TicketStateMachine
from client_support.policy.engine import PolicyEngine

class Phase0RunResult:
    def __init__(self, state: TicketState, policy_decision: str, events: list[str]) -> None:
        self.state = state
        self.policy_decision = policy_decision
        self.events = events

def run_demo_ticket(*, fuzzy_identity: bool = False) -> Phase0RunResult:
    machine = TicketStateMachine()
    events: list[str] = ["ticket.ingested"]
    machine.transition(TicketState.IDENTITY_PENDING)
    events.append("identity.pending")
    machine.transition(TicketState.IDENTITY_RESOLVED)
    events.append("identity.resolved")
    machine.transition(TicketState.ELIGIBILITY_CHECKED)
    events.append("ticket.eligibility_checked")
    machine.transition(TicketState.ROUTING_PENDING)
    events.append("routing.pending")
    machine.transition(TicketState.ROUTED)
    events.append("ticket.routed")
    machine.transition(TicketState.EXECUTION_PENDING)
    events.append("execution.pending")
    machine.transition(TicketState.POLICY_GATE)
    events.append("policy.gate")
    policy = PolicyEngine().evaluate(PolicyContext(
        identity_resolution_method="fuzzy" if fuzzy_identity else "exact_email",
        identity_confidence=0.9 if fuzzy_identity else 1.0,
        category_automation_level="full",
        proposed_action="draft_email",
    ))
    events.append("policy.evaluated")
    if policy.decision.value == "human_review":
        machine.transition(TicketState.HUMAN_REVIEW)
        events.append("review.required")
        return Phase0RunResult(machine.state, policy.decision.value, events)
    machine.transition(TicketState.COMPLETED)
    events.append("run.completed")
    return Phase0RunResult(machine.state, policy.decision.value, events)
