# Phase 1 — Order Tracking vertical slice

## Goal

Prove one end-to-end support capability before introducing a general-purpose Agent runtime.

## Flow

1. Ticket message enters the deterministic application boundary.
2. Customer identity is assumed resolved by the Phase 0 foundation.
3. The request is routed to `order_tracking`.
4. The category instructions define extraction and tool-use rules.
5. The subworkflow extracts order numbers.
6. `lookup_order` retrieves structured order data.
7. The application composes a response only from tool results.
8. Missing/unknown orders enter human review.

## Deliberate Phase 1 boundary

NextStep/LLM planning is not yet required for this single deterministic workflow. The application contract is designed so a future planner can choose the same subworkflow and tool without moving policy enforcement into the model.

## Definition of done

- happy-path order tracking test is green;
- missing order identifier is routed to human review;
- unknown order is routed to human review;
- no response invents order facts;
- category instructions live outside Python code;
- tool implementation is replaceable by a real ERP/CRM adapter;
- Phase 0 CI remains green.
