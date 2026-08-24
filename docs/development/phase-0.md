# Phase 0 development

## Local stack

1. Start PostgreSQL and pgvector:

   `docker compose up -d postgres`

2. Install the project:

   `pip install -e '.[dev]'`

3. Apply migrations:

   `alembic upgrade head`

4. Run checks:

   `ruff check .`
   `mypy src`
   `pytest`

## Evaluation

The current evaluation set is synthetic because production tickets are not available. Run the generator with:

`python -m evaluation.generate_phase0`

The generated data is intentionally small and deterministic. It validates the Phase 0 policy gate, especially exact identity versus fuzzy identity requiring human review.

A later evaluation phase will assess public datasets, including Hugging Face candidates, for semantic fit, licensing, privacy, and schema compatibility before incorporating any data.

## Temporal decision

Temporal is the selected durable workflow/queue technology for the architecture when long-running execution, durable retries, timers, resumable human approvals, or similar requirements appear. Phase 0 deliberately does not depend on Temporal because its deterministic execution path does not yet require those guarantees.
