import pytest
from client_support.domain.states import InvalidTransition, TicketState, TicketStateMachine

def test_valid_transition():
    machine = TicketStateMachine()
    machine.transition(TicketState.IDENTITY_PENDING)
    assert machine.state == TicketState.IDENTITY_PENDING

def test_invalid_transition_is_rejected():
    machine = TicketStateMachine()
    with pytest.raises(InvalidTransition):
        machine.transition(TicketState.COMPLETED)
