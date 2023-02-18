from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.response_header.v0.header import ResponseHeader
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ResponseHeader))
@settings(max_examples=1)
def test_response_header_roundtrip(instance: ResponseHeader) -> None:
    writer = entity_writer(ResponseHeader)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ResponseHeader))
    assert instance == result
