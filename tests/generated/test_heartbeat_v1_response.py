from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.heartbeat.v1.response import HeartbeatResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(HeartbeatResponse))
@settings(max_examples=1)
def test_heartbeat_response_roundtrip(instance: HeartbeatResponse) -> None:
    writer = entity_writer(HeartbeatResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(HeartbeatResponse))
    assert instance == result
