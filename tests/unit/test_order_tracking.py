from uuid import uuid4

from client_support.application.order_tracking import OrderTrackingApplication
from client_support.contracts.order_tracking import OrderRecord
from client_support.tools.order_lookup import OrderLookupTool


def app() -> OrderTrackingApplication:
    return OrderTrackingApplication(
        OrderLookupTool(
            records={
                "ORD-123456": OrderRecord(
                    order_number="ORD-123456",
                    status="in_transit",
                    carrier="Acme Carrier",
                    tracking_number="TRK-001",
                    estimated_delivery="2026-09-01",
                )
            }
        )
    )


def test_order_tracking_happy_path() -> None:
    result = app().execute(run_id=uuid4(), message="Where is order ORD-123456?")
    assert result.requires_human_review is False
    assert result.orders[0].status == "in_transit"
    assert "ORD-123456" in result.customer_message


def test_order_tracking_missing_identifier_goes_to_review() -> None:
    result = app().execute(run_id=uuid4(), message="Where is my package?")
    assert result.requires_human_review is True
    assert result.metadata["reason"] == "missing_order_number"


def test_order_tracking_unknown_order_goes_to_review() -> None:
    result = app().execute(run_id=uuid4(), message="Where is ORD-999999?")
    assert result.requires_human_review is True
    assert result.metadata["missing_order_numbers"] == ["ORD-999999"]
