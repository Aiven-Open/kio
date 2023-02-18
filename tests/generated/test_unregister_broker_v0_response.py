from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.unregister_broker.v0.response import UnregisterBrokerResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(UnregisterBrokerResponse))
@settings(max_examples=1)
def test_unregister_broker_response_roundtrip(
    instance: UnregisterBrokerResponse,
) -> None:
    writer = entity_writer(UnregisterBrokerResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UnregisterBrokerResponse))
    assert instance == result
