from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.broker_heartbeat.v0.response import BrokerHeartbeatResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(BrokerHeartbeatResponse))
@settings(max_examples=1)
def test_broker_heartbeat_response_roundtrip(instance: BrokerHeartbeatResponse) -> None:
    writer = entity_writer(BrokerHeartbeatResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(BrokerHeartbeatResponse))
    assert instance == result
