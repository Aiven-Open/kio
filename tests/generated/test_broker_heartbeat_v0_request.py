from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.broker_heartbeat.v0.request import BrokerHeartbeatRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(BrokerHeartbeatRequest))
@settings(max_examples=1)
def test_broker_heartbeat_request_roundtrip(instance: BrokerHeartbeatRequest) -> None:
    writer = entity_writer(BrokerHeartbeatRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(BrokerHeartbeatRequest))
    assert instance == result
