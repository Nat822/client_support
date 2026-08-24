# Phase 2.1 — NextStep execution loop

The first agent phase introduces a provider-neutral execution loop. The loop receives structured ticket context, asks a planner for the next step, executes typed tool calls through `ToolRuntime`, observes results, and repeats until completion or a safety limit is reached.

## Safety boundaries

The agent cannot call external systems directly. Every action goes through `ToolRuntime`. The first implementation has:

- a configurable maximum step count;
- repeated identical action detection;
- explicit blocked/failed terminal states;
- no customer-facing send operation;
- fake tools in tests only.

The planner is deliberately a protocol. A future NeuralDeep/OpenAI-compatible planner can be added without changing the execution loop.

## Next implementation steps

1. Add typed tool contracts and risk metadata.
2. Add deterministic `PolicyEngine` enforcement before `ToolRuntime` execution.
3. Add structured message log/telemetry.
4. Add an LLM-backed planner using the existing SGR provider boundary.
5. Add read-only CRM/helpdesk fake tools and end-to-end agent tests.

The 20-case SGR model comparison remains a production-readiness task, not a blocker for building the execution architecture.
