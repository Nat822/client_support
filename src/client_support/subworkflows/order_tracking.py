import re
from typing import Protocol

from client_support.contracts.order_tracking import OrderRecord, OrderTrackingRequest


class OrderLookup(Protocol):
    def lookup(self, order_number: str) -> OrderRecord | None: ...


ORDER_NUMBER_RE = re.compile(r"\b(?:ORD[-_ ]?)?\d{4,12}\b", re.IGNORECASE)


def extract_order_tracking_request(text: str, customer_id: str | None = None) -> OrderTrackingRequest:
    numbers = list(
        dict.fromkeys(
            match.group(0).upper().replace(" ", "-")
            for match in ORDER_NUMBER_RE.finditer(text)
        )
    )
    return OrderTrackingRequest(order_numbers=numbers, customer_id=customer_id, raw_request=text)


def execute_order_tracking(request: OrderTrackingRequest, lookup: OrderLookup) -> list[OrderRecord]:
    results: list[OrderRecord] = []
    for order_number in request.order_numbers:
        record = lookup.lookup(order_number)
        if record is not None:
            results.append(record)
    return results
