from client_support.domain.states import TicketState
from client_support.pipeline.demo_runner import run_demo_ticket

def test_phase0_demo_completes_without_review():
    result = run_demo_ticket()
    assert result.state == TicketState.COMPLETED
    assert result.policy_decision == "allow"
    assert result.events[-1] == "run.completed"

def test_phase0_demo_routes_fuzzy_identity_to_review():
    result = run_demo_ticket(fuzzy_identity=True)
    assert result.state == TicketState.HUMAN_REVIEW
    assert result.policy_decision == "human_review"
    assert result.events[-1] == "review.required"
