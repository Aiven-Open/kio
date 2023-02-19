from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sasl_handshake.v0.request import SaslHandshakeRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(SaslHandshakeRequest))
@settings(max_examples=1)
def test_sasl_handshake_request_roundtrip(instance: SaslHandshakeRequest) -> None:
    writer = entity_writer(SaslHandshakeRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SaslHandshakeRequest))
    assert instance == result
