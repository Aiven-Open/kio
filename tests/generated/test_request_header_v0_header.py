from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.request_header.v0.header import RequestHeader
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(RequestHeader))
@settings(max_examples=1)
def test_request_header_roundtrip(instance: RequestHeader) -> None:
    writer = entity_writer(RequestHeader)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(RequestHeader))
    assert instance == result
