from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.heartbeat.v4.request import HeartbeatRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_heartbeat_request: Final = entity_reader(HeartbeatRequest)


@given(from_type(HeartbeatRequest))
@settings(max_examples=1)
def test_heartbeat_request_roundtrip(instance: HeartbeatRequest) -> None:
    writer = entity_writer(HeartbeatRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_heartbeat_request(buffer)
    assert instance == result
