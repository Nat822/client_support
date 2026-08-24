from client_support.contracts.identity import IdentityResolutionMethod
from client_support.domain.run import RunStatus
from client_support.domain.states import TicketState
from client_support.pipeline.execution import Phase0Execution


def test_exact_identity_completes_deterministically() -> None:
    execution = Phase0Execution()
    run = execution.run(subject="Where is my order?", requester_email="customer@example.com")

    assert run.status is RunStatus.COMPLETED
    assert run.metadata["policy_decision"] == "allow"
    assert len(execution.events.list_for_run(run.id)) == 9


def test_fuzzy_identity_stops_at_human_review() -> None:
    execution = Phase0Execution()
    run = execution.run(
        subject="Where is my order?",
        requester_email="unknown@example.com",
        identity_method=IdentityResolutionMethod.FUZZY,
    )

    assert run.status is RunStatus.HUMAN_REVIEW
    assert execution.tickets.get(run.ticket_id).state is TicketState.HUMAN_REVIEW
    assert run.metadata["policy_decision"] == "human_review"
