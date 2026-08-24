# Phase 1 — Order Tracking runtime integration

The Order Tracking vertical slice is explicitly executed through the Phase 0 `ToolRuntime` safety boundary.

## Invariant

No order lookup handler is invoked directly by application code. The application creates a tool call and `ToolRuntime` enforces policy before the handler can execute.

```text
OrderTrackingRequest
  -> structured order extraction
  -> ToolRuntime
  -> PolicyEngine
  -> lookup_order
  -> ToolResult
```

Missing order identifiers are routed to human review before any tool call.

## Why this comes before an LLM agent

This establishes the deterministic execution contract that a future NextStep/SGR agent will use. The agent will plan tool calls, but it will not bypass `ToolRuntime` or the policy gate.
