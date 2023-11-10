from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.heartbeat.v3.response import HeartbeatResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_heartbeat_response: Final = entity_reader(HeartbeatResponse)


@given(from_type(HeartbeatResponse))
@settings(max_examples=1)
def test_heartbeat_response_roundtrip(instance: HeartbeatResponse) -> None:
    writer = entity_writer(HeartbeatResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_heartbeat_response(buffer)
    assert instance == result


@given(instance=from_type(HeartbeatResponse))
def test_heartbeat_response_java(
    instance: HeartbeatResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
