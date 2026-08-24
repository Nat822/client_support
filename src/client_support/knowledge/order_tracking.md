# Order Tracking

## Purpose
Handle requests asking where an order/package is or when it is expected to arrive.

## Required extraction
- `order_numbers`: one or more order identifiers found in the customer message.
- `customer_id`: resolved customer identifier when available.

## Tool
Use `lookup_order` for each extracted order number.

## Response rules
- Report only data returned by the order lookup tool.
- Do not invent carrier, tracking, or delivery dates.
- If an order number is missing, ask for it or route to human review.
- If any requested order cannot be found, route to human review.

## Automation level
Phase 1 fixture-backed implementation. Human review is required for unresolved order numbers or missing identifiers.
