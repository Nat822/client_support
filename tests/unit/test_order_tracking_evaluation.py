from client_support.contracts.sgr_provider import SGRClassification, SGRExtraction
from client_support.evaluation.order_tracking import OrderTrackingCase, evaluate_order_tracking


class FakeProvider:
    def classify(self, *, text: str) -> SGRClassification:
        category = "order_tracking" if "order" in text.lower() or "package" in text.lower() else "billing"
        return SGRClassification(category=category, confidence=0.99)

    def extract_order_tracking(self, *, text: str) -> SGRExtraction:
        numbers = [word.rstrip("?") for word in text.split() if word.startswith("ORD-")]
        return SGRExtraction(order_numbers=numbers, confidence=0.99)


def test_order_tracking_evaluation_reports_accuracy() -> None:
    cases = [
        OrderTrackingCase("Where is order ORD-001?", "order_tracking", ["ORD-001"]),
        OrderTrackingCase("Where is my package?", "order_tracking", []),
        OrderTrackingCase("Change my billing address", "billing", []),
    ]
    result = evaluate_order_tracking(FakeProvider(), cases)
    assert result.total == 3
    assert result.category_accuracy == 1.0
    assert result.extraction_accuracy == 1.0
