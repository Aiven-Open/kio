from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sasl_authenticate.v2.response import SaslAuthenticateResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(SaslAuthenticateResponse))
@settings(max_examples=1)
def test_sasl_authenticate_response_roundtrip(
    instance: SaslAuthenticateResponse,
) -> None:
    writer = entity_writer(SaslAuthenticateResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SaslAuthenticateResponse))
    assert instance == result
