from dataclasses import dataclass

from client_support.contracts.sgr_provider import SGRProvider


@dataclass(frozen=True, slots=True)
class OrderTrackingCase:
    text: str
    expected_category: str
    expected_order_numbers: list[str]


@dataclass(frozen=True, slots=True)
class OrderTrackingEvaluation:
    total: int
    category_accuracy: float
    extraction_accuracy: float


def evaluate_order_tracking(provider: SGRProvider, cases: list[OrderTrackingCase]) -> OrderTrackingEvaluation:
    if not cases:
        return OrderTrackingEvaluation(0, 0.0, 0.0)

    category_hits = 0
    extraction_hits = 0
    for case in cases:
        classification = provider.classify(text=case.text)
        extraction = provider.extract_order_tracking(text=case.text)
        category_hits += classification.category == case.expected_category
        extraction_hits += sorted(extraction.order_numbers) == sorted(case.expected_order_numbers)

    total = len(cases)
    return OrderTrackingEvaluation(
        total=total,
        category_accuracy=category_hits / total,
        extraction_accuracy=extraction_hits / total,
    )
