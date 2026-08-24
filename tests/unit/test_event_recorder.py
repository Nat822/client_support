from uuid import uuid4

from client_support.telemetry import EventRecorder


def test_event_recorder_assigns_order_and_utc_timestamp() -> None:
    recorder = EventRecorder()
    run_id = uuid4()
    ticket_id = uuid4()

    event = recorder.record(
        run_id=run_id,
        ticket_id=ticket_id,
        sequence=1,
        event_type="ticket.ingested",
    )

    assert event.sequence == 1
    assert event.run_id == run_id
    assert event.ticket_id == ticket_id
    assert event.created_at.tzinfo is not None
    assert len(recorder.events) == 1
