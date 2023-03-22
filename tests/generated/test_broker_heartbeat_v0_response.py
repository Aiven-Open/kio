from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.broker_heartbeat.v0.response import BrokerHeartbeatResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_broker_heartbeat_response: Final = entity_reader(BrokerHeartbeatResponse)


@given(from_type(BrokerHeartbeatResponse))
@settings(max_examples=1)
def test_broker_heartbeat_response_roundtrip(instance: BrokerHeartbeatResponse) -> None:
    writer = entity_writer(BrokerHeartbeatResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_broker_heartbeat_response(buffer)
    assert instance == result
