from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class AgentEvent:
    event_type: str
    run_id: str
    sequence: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    payload: dict[str, Any] = field(default_factory=dict)


class InMemoryEventLog:
    def __init__(self) -> None:
        self._events: list[AgentEvent] = []

    def append(self, event: AgentEvent) -> None:
        self._events.append(event)

    def events(self, run_id: str | None = None) -> list[AgentEvent]:
        if run_id is None:
            return list(self._events)
        return [event for event in self._events if event.run_id == run_id]
