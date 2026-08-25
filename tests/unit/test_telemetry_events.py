from client_support.telemetry.events import AgentEvent, InMemoryEventLog


def test_event_log_preserves_sequence_and_filters_run() -> None:
    log = InMemoryEventLog()
    log.append(AgentEvent("run_started", "r1", 0))
    log.append(AgentEvent("tool_call", "r1", 1, payload={"tool": "lookup_order"}))
    log.append(AgentEvent("run_started", "r2", 0))

    assert [event.event_type for event in log.events("r1")] == ["run_started", "tool_call"]
    assert log.events("r1")[1].payload["tool"] == "lookup_order"
    assert len(log.events()) == 3
