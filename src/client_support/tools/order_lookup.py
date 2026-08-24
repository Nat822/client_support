from dataclasses import dataclass

from client_support.contracts.order_tracking import OrderRecord


@dataclass(frozen=True, slots=True)
class OrderLookupTool:
    """Phase 1 smart tool: deterministic fixture-backed order lookup."""

    records: dict[str, OrderRecord]

    name: str = "lookup_order"

    def lookup(self, order_number: str) -> OrderRecord | None:
        return self.records.get(order_number.upper())

    def execute(self, order_number: str) -> OrderRecord | None:
        return self.lookup(order_number)
