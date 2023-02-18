from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.heartbeat.v0.request import HeartbeatRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(HeartbeatRequest))
@settings(max_examples=1)
def test_heartbeat_request_roundtrip(instance: HeartbeatRequest) -> None:
    writer = entity_writer(HeartbeatRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(HeartbeatRequest))
    assert instance == result
