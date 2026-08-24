# Phase 1 — SGR adapter and evaluation

This increment introduces a provider-neutral SGR boundary without coupling the application to a specific model vendor.

## Boundary

`SGRProvider` exposes two operations:

- classification into the ticket taxonomy;
- structured extraction for Order Tracking.

The provider is intentionally outside the policy and tool layers. A model may propose a category or extracted order number, but deterministic PolicyEngine and ToolRuntime remain authoritative for execution.

## Evaluation

`evaluation/order_tracking.jsonl` is a small synthetic golden set used because production tickets are not available yet. It includes positive Order Tracking cases, missing-order-number cases, and a non-Order-Tracking case.

Metrics:

- category accuracy;
- exact extraction accuracy.

The fake provider in unit tests validates the evaluation harness itself. It is not a production model and must not be treated as evidence of model quality.

Before selecting a real model, add provider-specific adapters and compare them against this dataset plus a larger reviewed dataset. Any public Hugging Face dataset must be screened for license, privacy, relevance, and leakage before adoption.
