from dataclasses import dataclass, field
from uuid import UUID

from client_support.contracts.identity import CustomerRef
from client_support.domain.states import TicketState


@dataclass(slots=True)
class Ticket:
    id: UUID
    subject: str
    requester_email: str
    state: TicketState = TicketState.INGESTED
    customer: CustomerRef | None = None
    category: str | None = None
    support_level: str | None = None
    metadata: dict[str, object] = field(default_factory=dict)
