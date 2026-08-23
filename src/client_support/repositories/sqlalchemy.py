from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from client_support.domain.run import ExecutionRun
from client_support.domain.ticket import Ticket
from client_support.persistence.models import EventModel, RunModel, TicketModel
from client_support.telemetry import DomainEvent


class SqlAlchemyTicketRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, ticket: Ticket) -> None:
        self.session.add(
            TicketModel(
                id=ticket.id,
                subject=ticket.subject,
                requester_email=ticket.requester_email,
                state=ticket.state.value,
                category=ticket.category,
                support_level=ticket.support_level,
                metadata_json=ticket.metadata,
            )
        )

    def get(self, ticket_id: UUID) -> Ticket | None:
        model = self.session.get(TicketModel, ticket_id)
        if model is None:
            return None
        return Ticket(
            id=model.id,
            subject=model.subject,
            requester_email=model.requester_email,
            state=model.state,
            category=model.category,
            support_level=model.support_level,
            metadata=model.metadata_json,
        )


class SqlAlchemyRunRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, run: ExecutionRun) -> None:
        self.session.add(
            RunModel(
                id=run.id,
                ticket_id=run.ticket_id,
                status=run.status.value,
                metadata_json=run.metadata,
            )
        )

    def get(self, run_id: UUID) -> ExecutionRun | None:
        model = self.session.get(RunModel, run_id)
        if model is None:
            return None
        return ExecutionRun(
            id=model.id,
            ticket_id=model.ticket_id,
            status=model.status,
            metadata=model.metadata_json,
        )


class SqlAlchemyEventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def append(self, event: DomainEvent) -> None:
        self.session.add(
            EventModel(
                id=event.event_id,
                run_id=event.run_id,
                ticket_id=event.ticket_id,
                sequence=event.sequence,
                event_type=event.event_type,
                payload=event.payload,
                created_at=event.created_at,
            )
        )

    def list_for_run(self, run_id: UUID) -> list[DomainEvent]:
        models = self.session.scalars(
            select(EventModel).where(EventModel.run_id == run_id).order_by(EventModel.sequence)
        ).all()
        return [
            DomainEvent(
                event_id=model.id,
                run_id=model.run_id,
                ticket_id=model.ticket_id,
                sequence=model.sequence,
                event_type=model.event_type,
                payload=model.payload,
                created_at=model.created_at,
            )
            for model in models
        ]
