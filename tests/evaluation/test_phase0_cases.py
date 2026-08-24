from client_support.contracts.identity import IdentityResolutionMethod
from client_support.domain.run import RunStatus
from client_support.pipeline.execution import Phase0Execution


def test_phase0_golden_cases() -> None:
    execution = Phase0Execution()
    cases = [
        (IdentityResolutionMethod.EXACT_EMAIL, RunStatus.COMPLETED, "allow"),
        (IdentityResolutionMethod.FUZZY, RunStatus.HUMAN_REVIEW, "human_review"),
    ]

    for identity_method, expected_status, expected_policy in cases:
        run = execution.run(
            subject="Synthetic evaluation ticket",
            requester_email="synthetic@example.com",
            identity_method=identity_method,
        )
        assert run.status is expected_status
        assert run.metadata["policy_decision"] == expected_policy
