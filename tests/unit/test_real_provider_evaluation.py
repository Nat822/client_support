from client_support.contracts.sgr_provider import SGRClassification, SGRExtraction
from client_support.evaluation.order_tracking import OrderTrackingCase
from client_support.evaluation.real_provider import evaluate_real_provider


class FakeProvider:
    def classify(self, *, text: str) -> SGRClassification:
        return SGRClassification(category="order_tracking", confidence=0.9)

    def extract_order_tracking(self, *, text: str) -> SGRExtraction:
        return SGRExtraction(order_numbers=["ORD-001"], confidence=0.9)


def test_real_provider_evaluation_collects_quality_and_latency_metrics() -> None:
    result = evaluate_real_provider(
        FakeProvider(),
        [OrderTrackingCase("Where is ORD-001?", "order_tracking", ["ORD-001"])],
    )
    assert result.total == 1
    assert result.category_accuracy == 1.0
    assert result.extraction_accuracy == 1.0
    assert result.error_rate == 0.0
    assert result.average_latency_seconds >= 0.0
