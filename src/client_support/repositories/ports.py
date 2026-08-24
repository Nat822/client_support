from typing import Protocol
from uuid import UUID

from client_support.domain.run import ExecutionRun
from client_support.domain.ticket import Ticket
from client_support.telemetry import DomainEvent


class TicketRepository(Protocol):
    def add(self, ticket: Ticket) -> None: ...
    def get(self, ticket_id: UUID) -> Ticket | None: ...


class RunRepository(Protocol):
    def add(self, run: ExecutionRun) -> None: ...
    def get(self, run_id: UUID) -> ExecutionRun | None: ...


class EventRepository(Protocol):
    def append(self, event: DomainEvent) -> None: ...
    def list_for_run(self, run_id: UUID) -> list[DomainEvent]: ...
