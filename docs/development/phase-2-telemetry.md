# Phase 2.6 — Structured agent telemetry

The agent execution path now has a typed event primitive for MessageLog/I telemetry.

`AgentEvent` records a stable `event_type`, `run_id`, monotonic `sequence`, UTC timestamp, and structured payload. `InMemoryEventLog` is the initial adapter for tests and local execution.

The event schema is intentionally provider-agnostic. It can later be persisted to Postgres/JSONL or streamed through Temporal without changing agent code.

Recommended event types for the execution loop:

- `run_started`
- `plan_received`
- `tool_call_requested`
- `policy_decision`
- `tool_result`
- `context_compacted`
- `run_completed`
- `run_failed`

Do not log secrets, authorization headers, raw customer PII, or complete LLM prompts by default. Payloads should contain structured references and sanitized metadata.
