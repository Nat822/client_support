from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field

class TicketStatus(StrEnum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Message(BaseModel):
    id: str
    sender_email: str
    body: str
    created_at: datetime

class Attachment(BaseModel):
    id: str
    filename: str
    content_type: str
    size_bytes: int = Field(ge=0)

class TicketIngested(BaseModel):
    ticket_id: str
    source: str
    subject: str
    status: TicketStatus
    messages: list[Message]
    attachments: list[Attachment] = []
