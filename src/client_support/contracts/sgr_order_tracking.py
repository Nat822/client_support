from dataclasses import dataclass
from enum import StrEnum


class TicketCategory(StrEnum):
    ORDER_TRACKING = "order_tracking"
    UNSUPPORTED = "unsupported"


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    category: TicketCategory
    confidence: float


@dataclass(frozen=True, slots=True)
class OrderTrackingExtraction:
    order_numbers: list[str]


class OrderTrackingClassifier:
    """Deterministic stand-in for the SGR classifier boundary."""

    def classify(self, message: str) -> ClassificationResult:
        lowered = message.lower()
        if "order" in lowered or "package" in lowered or "delivery" in lowered:
            return ClassificationResult(TicketCategory.ORDER_TRACKING, 1.0)
        return ClassificationResult(TicketCategory.UNSUPPORTED, 1.0)


class OrderTrackingExtractor:
    """Structured extraction contract; an LLM/SGR adapter can implement it later."""

    def extract(self, message: str) -> OrderTrackingExtraction:
        import re

        return OrderTrackingExtraction(order_numbers=re.findall(r"\bORD-\d+\b", message.upper()))
