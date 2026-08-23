from datetime import datetime
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TicketModel(Base):
    __tablename__ = "tickets"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    subject: Mapped[str] = mapped_column(Text)
    requester_email: Mapped[str] = mapped_column(String(320), index=True)
    state: Mapped[str] = mapped_column(String(64), index=True)
    category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    support_level: Mapped[str | None] = mapped_column(String(32), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    external_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RunModel(Base):
    __tablename__ = "runs"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    ticket_id: Mapped[UUID] = mapped_column(ForeignKey("tickets.id"), index=True)
    status: Mapped[str] = mapped_column(String(64), index=True)
    agent_version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    routing_version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    policy_version: Mapped[str | None] = mapped_column(String(255), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("runs.id"), index=True)
    ticket_id: Mapped[UUID] = mapped_column(ForeignKey("tickets.id"), index=True)
    sequence: Mapped[int] = mapped_column(Integer)
    event_type: Mapped[str] = mapped_column(String(255), index=True)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ToolCallModel(Base):
    __tablename__ = "tool_calls"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("runs.id"), index=True)
    tool_name: Mapped[str] = mapped_column(String(255), index=True)
    status: Mapped[str] = mapped_column(String(64))
    risk_level: Mapped[str] = mapped_column(String(32))
    request: Mapped[dict] = mapped_column(JSONB, default=dict)
    result: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class PolicyDecisionModel(Base):
    __tablename__ = "policy_decisions"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    run_id: Mapped[UUID] = mapped_column(ForeignKey("runs.id"), index=True)
    decision: Mapped[str] = mapped_column(String(32))
    reasons: Mapped[list] = mapped_column(JSONB, default=list)
    context: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class KnowledgeItemModel(Base):
    __tablename__ = "knowledge_items"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True)
    category: Mapped[str] = mapped_column(String(255), index=True)
    version: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class EvaluationCaseModel(Base):
    __tablename__ = "evaluation_cases"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    input_data: Mapped[dict] = mapped_column(JSONB)
    expected: Mapped[dict] = mapped_column(JSONB)
    source: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
