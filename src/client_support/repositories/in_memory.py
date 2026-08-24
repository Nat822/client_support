from uuid import UUID

from client_support.domain.run import ExecutionRun
from client_support.domain.ticket import Ticket
from client_support.telemetry import DomainEvent


class InMemoryTicketRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, Ticket] = {}

    def add(self, ticket: Ticket) -> None:
        self._items[ticket.id] = ticket

    def get(self, ticket_id: UUID) -> Ticket | None:
        return self._items.get(ticket_id)


class InMemoryRunRepository:
    def __init__(self) -> None:
        self._items: dict[UUID, ExecutionRun] = {}

    def add(self, run: ExecutionRun) -> None:
        self._items[run.id] = run

    def get(self, run_id: UUID) -> ExecutionRun | None:
        return self._items.get(run_id)


class InMemoryEventRepository:
    def __init__(self) -> None:
        self._items: list[DomainEvent] = []

    def append(self, event: DomainEvent) -> None:
        self._items.append(event)

    def list_for_run(self, run_id: UUID) -> list[DomainEvent]:
        return [event for event in self._items if event.run_id == run_id]
