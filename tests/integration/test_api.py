from fastapi.testclient import TestClient

from client_support.api.app import app

client = TestClient(app)


def test_phase0_api_returns_reproducible_execution_shape() -> None:
    response = client.post(
        "/v1/phase0/run",
        json={"subject": "Where is my order?", "requester_email": "customer@example.com"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["state"] == "completed"
    assert body["events"][-1]["type"] == "run.completed"


def test_phase0_api_routes_fuzzy_identity_to_review() -> None:
    response = client.post(
        "/v1/phase0/run",
        json={
            "subject": "Where is my order?",
            "requester_email": "customer@example.com",
            "identity_method": "fuzzy",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "human_review"
    assert body["state"] == "human_review"
    assert body["metadata"]["policy_decision"] == "human_review"
