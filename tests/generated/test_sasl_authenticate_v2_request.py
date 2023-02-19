from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sasl_authenticate.v2.request import SaslAuthenticateRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(SaslAuthenticateRequest))
@settings(max_examples=1)
def test_sasl_authenticate_request_roundtrip(instance: SaslAuthenticateRequest) -> None:
    writer = entity_writer(SaslAuthenticateRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SaslAuthenticateRequest))
    assert instance == result
