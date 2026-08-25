# Phase 2.5 — live NeuralDeep agent E2E

The first end-to-end agent path is now wired as:

`NeuralDeep planner -> NextStepAgent -> PolicyAwareToolRuntime -> PolicyEngine -> read-only tool -> observation -> planner`

The E2E smoke intentionally uses one deterministic local `lookup_order` handler so no CRM/ERP or customer-facing system is touched. **Planning is live NeuralDeep**; there is no fake LLM response.

## Safety boundary

Only a `READ` tool is registered. The existing PolicyEngine remains authoritative. A write or customer-facing action cannot execute through this smoke.

## Validation

Use the `NeuralDeep Agent E2E` manual workflow with `NEURALDEEP_API_KEY` and the selected NeuralDeep model. The expected terminal state is `completed` after at least one real planner/tool/observation cycle.

This is the first integration proof of the G/H architecture, but it is not production readiness: real CRM/ERP adapters, review gates, message telemetry, retries, and broader evaluation remain future work.
