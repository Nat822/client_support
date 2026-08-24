# Order Tracking

## Category

Use this category for questions about order status, shipment progress, delivery, or package location.

## SGR extraction

Extract order identifiers when present. Preserve the original identifier and do not invent one.

## Required fields

- `order_numbers`

## Routing

- Supported category: `order_tracking`
- Missing order number: continue to human review unless another trusted lookup key is available.
- Multiple order numbers: resolve each explicitly or request clarification.

## Response guidance

Only state order information returned by the authorized order lookup tool. Do not infer delivery dates or invent tracking events.
