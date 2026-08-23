from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID


class RunStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    HUMAN_REVIEW = "human_review"


@dataclass(slots=True)
class ExecutionRun:
    id: UUID
    ticket_id: UUID
    status: RunStatus = RunStatus.RUNNING
    sequence: int = 0
    metadata: dict[str, object] = field(default_factory=dict)
