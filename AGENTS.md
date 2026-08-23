# AGENTS.md — Client Support AI

## Mission
Build a production-shaped Client Support AI foundation using a modular monolith, deterministic workflow boundaries, explicit contracts, auditable agent execution, and measurable evaluation.

## Architecture baseline
- Python 3.13
- FastAPI
- Pydantic 2
- SQLAlchemy 2 + Alembic
- PostgreSQL + pgvector
- pytest + Ruff + static type checking
- OpenTelemetry plus a first-class domain execution-event model
- Docker / Docker Compose for local development
- GitHub Actions for CI
- LLM provider abstraction; do not couple the domain to a single provider
- Temporal is the chosen future durable workflow/queue solution if execution complexity requires durable waits, retries, human approvals, or resumable long-running workflows. Do not introduce Temporal in Phase 0 without evidence that it is needed.

## Non-negotiable boundaries
1. `contracts/` contains boundary/API/integration schemas. `domain/` contains internal business concepts. External payloads must not dictate domain models.
2. Agent proposes actions; Policy authorizes; Tool Runtime enforces; Telemetry records.
3. The agent must not bypass Policy to perform side-effecting operations.
4. Domain code must not depend on API or integration implementations.
5. Phase 0 must run without an LLM and without real external integrations.
6. Do not introduce microservices, Kafka, Kubernetes, a separate vector database, or a workflow engine until a concrete requirement justifies them.
7. Do not make LangChain or another orchestration framework the architectural core.
8. Knowledge changes are versioned and validated before production retrieval.
9. Never put raw customer/PII-heavy payloads into general telemetry by default; store references or minimized structured facts.

## Phase 0 definition of done
A fake ticket can be submitted to the API and traverse a deterministic pipeline that:
- creates a ticket and run;
- performs explicit state transitions;
- persists an ordered execution trace;
- evaluates policy;
- persists tool-call and policy-decision records where applicable;
- returns a reproducible result;
- is covered by unit, integration, contract, and architecture tests.

A small generated/golden evaluation dataset must also exist. We currently have no real tickets, so fixtures must be synthetic and clearly labeled. Later, suitable public datasets (including Hugging Face) may be evaluated for relevance and licensing.

## Coding practices
- Prefer small typed functions and explicit dependencies.
- Keep business rules deterministic where possible.
- Validate at boundaries.
- Use dependency inversion for repositories, clocks, IDs, integrations, and tools.
- Avoid global mutable state.
- Use UTC timestamps.
- Make side effects explicit.
- Write tests with behavior-focused names.
- Add an ADR when changing a major architectural invariant or introducing infrastructure.
- Keep README/docs aligned with implemented behavior.

## Testing
Required layers:
- unit tests for domain/state/policy/contracts;
- integration tests for PostgreSQL/repositories/API;
- contract tests for external adapters;
- architecture tests for import/dependency boundaries;
- evaluation tests for golden cases.

## Git workflow
- Use small, reviewable commits.
- Prefer feature branches and pull requests for substantial changes.
- Do not silently change architectural decisions while implementing; document changes in `docs/architecture/` or ADRs.
