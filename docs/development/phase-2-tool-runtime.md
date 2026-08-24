# Phase 2.3 — Policy-aware ToolRuntime

The NextStep execution loop now has a concrete runtime boundary that resolves requested tool names through a registry and evaluates the registered tool with `PolicyEngine` before invoking its handler.

Flow:

```text
Agent -> ToolCall -> ToolRegistry -> PolicyEngine -> ToolHandler -> ToolResult
```

Unknown tools and policy-denied tools become structured `ToolResult` observations rather than exceptions escaping into the agent loop.

This phase still uses in-process fake handlers. External CRM/ERP/helpdesk adapters are deliberately deferred until the policy boundary is proven by tests.
