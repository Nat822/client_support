# Phase 1 — controlled SGR boundary

The Order Tracking vertical slice now has an explicit classification and structured-extraction boundary.

This phase intentionally does **not** introduce an autonomous NextStep Agent or an LLM dependency. The classifier and extractor are deterministic implementations of the contracts so the execution architecture can be tested first.

## Intended evolution

```text
Ticket
  -> classifier contract
  -> TicketCategory
  -> category instructions
  -> structured extraction contract
  -> deterministic PolicyEngine
  -> ToolRuntime
  -> authorized tool
```

A future SGR adapter can replace the deterministic classifier/extractor without changing contracts, policy, or ToolRuntime.
