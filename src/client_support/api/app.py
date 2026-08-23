from fastapi import FastAPI
from client_support.contracts.policy import PolicyContext
from client_support.domain.states import TicketState, TicketStateMachine
from client_support.policy.engine import PolicyEngine

app = FastAPI(title="Client Support AI", version="0.1.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/v1/phase0/demo")
def phase0_demo() -> dict[str, object]:
    machine = TicketStateMachine()
    machine.transition(TicketState.IDENTITY_PENDING)
    machine.transition(TicketState.IDENTITY_RESOLVED)
    machine.transition(TicketState.ELIGIBILITY_CHECKED)
    machine.transition(TicketState.ROUTING_PENDING)
    machine.transition(TicketState.ROUTED)
    machine.transition(TicketState.EXECUTION_PENDING)
    machine.transition(TicketState.POLICY_GATE)
    policy = PolicyEngine().evaluate(PolicyContext(
        identity_resolution_method="exact_email",
        identity_confidence=1.0,
        category_automation_level="full",
        proposed_action="draft_email",
    ))
    machine.transition(TicketState.COMPLETED)
    return {"state": machine.state, "policy": policy.model_dump()}
