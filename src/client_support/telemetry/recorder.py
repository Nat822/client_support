from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class DomainEvent:
    event_id: UUID
    run_id: UUID
    ticket_id: UUID
    sequence: int
    event_type: str
    payload: dict[str, Any]
    created_at: datetime


class EventRecorder:
    """In-memory Phase 0 recorder; persistence is added by the repository layer."""

    def __init__(self, sink: Callable[[DomainEvent], None] | None = None) -> None:
        self.events: list[DomainEvent] = []
        self._sink = sink

    def record(
        self,
        *,
        run_id: UUID,
        ticket_id: UUID,
        sequence: int,
        event_type: str,
        payload: dict[str, Any] | None = None,
    ) -> DomainEvent:
        event = DomainEvent(
            event_id=uuid4(),
            run_id=run_id,
            ticket_id=ticket_id,
            sequence=sequence,
            event_type=event_type,
            payload=payload or {},
            created_at=datetime.now(timezone.utc),
        )
        self.events.append(event)
        if self._sink:
            self._sink(event)
        return event
