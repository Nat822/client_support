from enum import StrEnum


class TicketState(StrEnum):
    INGESTED = "ingested"
    IDENTITY_PENDING = "identity_pending"
    IDENTITY_RESOLVED = "identity_resolved"
    ELIGIBILITY_CHECKED = "eligibility_checked"
    ROUTING_PENDING = "routing_pending"
    ROUTED = "routed"
    EXECUTION_PENDING = "execution_pending"
    POLICY_GATE = "policy_gate"
    HUMAN_REVIEW = "human_review"
    COMPLETED = "completed"


_ALLOWED: dict[TicketState, set[TicketState]] = {
    TicketState.INGESTED: {TicketState.IDENTITY_PENDING},
    TicketState.IDENTITY_PENDING: {TicketState.IDENTITY_RESOLVED, TicketState.HUMAN_REVIEW},
    TicketState.IDENTITY_RESOLVED: {TicketState.ELIGIBILITY_CHECKED},
    TicketState.ELIGIBILITY_CHECKED: {TicketState.ROUTING_PENDING, TicketState.HUMAN_REVIEW},
    TicketState.ROUTING_PENDING: {TicketState.ROUTED, TicketState.HUMAN_REVIEW},
    TicketState.ROUTED: {TicketState.EXECUTION_PENDING, TicketState.HUMAN_REVIEW},
    TicketState.EXECUTION_PENDING: {TicketState.POLICY_GATE, TicketState.HUMAN_REVIEW},
    TicketState.POLICY_GATE: {TicketState.COMPLETED, TicketState.HUMAN_REVIEW},
    TicketState.HUMAN_REVIEW: {TicketState.COMPLETED},
    TicketState.COMPLETED: set(),
}


def can_transition(current: TicketState, target: TicketState) -> bool:
    return target in _ALLOWED[current]


class InvalidTransition(ValueError):
    pass


class TicketStateMachine:
    def __init__(self, state: TicketState = TicketState.INGESTED) -> None:
        self.state = state

    def transition(self, target: TicketState) -> TicketState:
        if not can_transition(self.state, target):
            raise InvalidTransition(f"Cannot transition {self.state} -> {target}")
        self.state = target
        return self.state
