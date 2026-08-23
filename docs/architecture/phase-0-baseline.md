# Phase 0 Architecture Baseline

## Purpose
Phase 0 is an executable foundation, not an AI-agent implementation. It establishes stable boundaries and observability so the first vertical slice can be built without reworking the core.

## Stack
- Python 3.13
- FastAPI + Pydantic 2
- SQLAlchemy 2 + Alembic
- PostgreSQL + pgvector
- pytest, Ruff, static type checking
- OpenTelemetry + domain execution events
- Docker Compose locally; GitHub Actions in CI

## Architecture
```text
FastAPI
  -> Application Services
      -> Contracts
      -> Domain
      -> State Machine
      -> Policy Engine
      -> Tool Registry
      -> Repositories
      -> Telemetry
          -> PostgreSQL
```

The system is a modular monolith. Modules have explicit dependency boundaries; deployment is intentionally simple until scaling evidence requires otherwise.

## Contracts vs domain
`contracts/` models data crossing a boundary: API requests/responses, integration payloads, tool requests/results, policy decisions, and event envelopes.

`domain/` models internal concepts and business invariants. Domain code must not import concrete API or integration adapters.

This separation prevents an external helpdesk/CRM schema from becoming the internal business model.

## State and execution
Phase 0 contains a deterministic ticket/run state machine. It does not depend on an LLM. Agent execution will be added later behind an execution boundary.

The future execution flow is:

```text
Router F
  -> Agent G proposes action
  -> Policy J authorizes/denies/requires review
  -> Tool Runtime H enforces authorization and executes
  -> Event/Trace I records the result
```

The agent never becomes the authorization layer.

## Policy
Policy is an independent domain/application component. It evaluates identity resolution method, category support level, action risk, and other deterministic facts. It can return `ALLOW`, `DENY`, or `HUMAN_REVIEW`.

## Tools
Tools have explicit contracts and metadata including risk level, side effects, required inputs, and outputs. Tool runtime enforcement is separate from agent planning.

## Database model
Phase 0 uses PostgreSQL as the operational system of record. Initial tables are:

- `tickets`
- `customers`
- `runs`
- `events`
- `tool_calls`
- `policy_decisions`
- `knowledge_items`
- `evaluation_cases`

pgvector is selected for the future hybrid retrieval layer. PostgreSQL full-text search plus vector similarity gives a single-store starting point for the knowledge layer.

## Evaluation data
No real tickets or cases are currently available. Phase 0 therefore creates synthetic, labeled golden fixtures. We will also investigate public datasets, including Hugging Face, for suitable support/customer-service examples, subject to relevance, licensing, and schema quality. Public datasets will supplement rather than silently replace our generated cases.

## Testing strategy
- Unit: domain, contracts, state machine, policy.
- Integration: PostgreSQL, repositories, API.
- Contract: external adapters and tool interfaces.
- Architecture: import/dependency rules.
- Evaluation: golden cases and deterministic expected outcomes.

## Definition of Done
A fake ticket can be submitted through the API and traverse the deterministic foundation, creating a run, making explicit state transitions, persisting an ordered trace, evaluating policy, and producing a reproducible result. Tests cover the required layers. The run works without an LLM and without real external systems.

## Workflow/queue decision
**Temporal is the chosen future solution if durable workflow capabilities become necessary.** Evidence that would trigger its introduction includes long-running agent executions, durable waits, human approval/resume, complex retries, scheduled continuation, or workflow recovery requirements that exceed the Phase 0 execution runner.

Temporal is deliberately not part of Phase 0. We first prove the workflow shape with a simple application runner and persistent state/events.

## Deliberate non-goals
- microservices
- Kubernetes
- Kafka
- separate vector database
- separate search engine
- multi-agent orchestration
- autonomous customer email sending
- production self-learning
- framework-centric agent architecture
