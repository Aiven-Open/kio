from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.broker_registration.v0.request import Listener
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(Listener))
@settings(max_examples=1)
def test_listener_roundtrip(instance: Listener) -> None:
    writer = entity_writer(Listener)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(Listener))
    assert instance == result


from kio.schema.broker_registration.v0.request import Feature


@given(from_type(Feature))
@settings(max_examples=1)
def test_feature_roundtrip(instance: Feature) -> None:
    writer = entity_writer(Feature)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(Feature))
    assert instance == result


from kio.schema.broker_registration.v0.request import BrokerRegistrationRequest


@given(from_type(BrokerRegistrationRequest))
@settings(max_examples=1)
def test_broker_registration_request_roundtrip(
    instance: BrokerRegistrationRequest,
) -> None:
    writer = entity_writer(BrokerRegistrationRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(BrokerRegistrationRequest))
    assert instance == result
