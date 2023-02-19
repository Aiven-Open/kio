from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.broker_registration.v0.response import BrokerRegistrationResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(BrokerRegistrationResponse))
@settings(max_examples=1)
def test_broker_registration_response_roundtrip(
    instance: BrokerRegistrationResponse,
) -> None:
    writer = entity_writer(BrokerRegistrationResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(BrokerRegistrationResponse))
    assert instance == result
