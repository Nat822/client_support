# Phase 2.2 — Tool contracts and PolicyEngine

Tool execution is governed by a deterministic policy boundary outside the LLM.

## Risk classes

- `read`: read-only operations; allowed by default.
- `write`: mutations; blocked by default. Even when writes are enabled, they require human review in this phase.
- `customer_facing`: outbound customer actions; always require human review in this phase.

The agent proposes a `ToolCall`; it does not grant itself permission. A later integration will resolve the call to a registered `ToolDefinition`, evaluate it with `PolicyEngine`, and only then invoke `ToolRuntime` when allowed.

This is intentionally conservative. Production policy can later use ticket status, account resolution confidence, category automation level, and tool-specific risk, but those rules should remain deterministic and testable rather than delegated to the model.
