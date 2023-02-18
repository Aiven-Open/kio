from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sasl_handshake.v0.response import SaslHandshakeResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(SaslHandshakeResponse))
@settings(max_examples=1)
def test_sasl_handshake_response_roundtrip(instance: SaslHandshakeResponse) -> None:
    writer = entity_writer(SaslHandshakeResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SaslHandshakeResponse))
    assert instance == result
