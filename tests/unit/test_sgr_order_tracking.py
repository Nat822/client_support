from client_support.contracts.sgr_order_tracking import (
    OrderTrackingClassifier,
    OrderTrackingExtractor,
    TicketCategory,
)


def test_classifier_routes_order_language() -> None:
    result = OrderTrackingClassifier().classify("Where is my package for order ORD-001?")
    assert result.category is TicketCategory.ORDER_TRACKING
    assert result.confidence == 1.0


def test_classifier_rejects_unsupported_request() -> None:
    result = OrderTrackingClassifier().classify("How do I change my password?")
    assert result.category is TicketCategory.UNSUPPORTED


def test_extractor_returns_structured_order_numbers() -> None:
    result = OrderTrackingExtractor().extract("Please check ORD-001 and ORD-002")
    assert result.order_numbers == ["ORD-001", "ORD-002"]
