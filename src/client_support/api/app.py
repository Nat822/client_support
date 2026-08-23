from fastapi import FastAPI
from pydantic import BaseModel

from client_support.contracts.identity import IdentityResolutionMethod
from client_support.pipeline.execution import Phase0Execution

app = FastAPI(title="Client Support AI", version="0.1.0")
execution = Phase0Execution()


class Phase0TicketRequest(BaseModel):
    subject: str
    requester_email: str
    identity_method: IdentityResolutionMethod = IdentityResolutionMethod.EXACT_EMAIL


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/phase0/run")
def phase0_run(request: Phase0TicketRequest) -> dict[str, object]:
    run = execution.run(
        subject=request.subject,
        requester_email=request.requester_email,
        identity_method=request.identity_method,
    )
    ticket = execution.tickets.get(run.ticket_id)
    events = execution.events.list_for_run(run.id)
    return {
        "ticket_id": str(run.ticket_id),
        "run_id": str(run.id),
        "state": ticket.state.value if ticket else None,
        "status": run.status.value,
        "metadata": run.metadata,
        "events": [
            {
                "sequence": event.sequence,
                "type": event.event_type,
                "payload": event.payload,
            }
            for event in events
        ],
    }
