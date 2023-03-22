from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.response_header.v1.header import ResponseHeader
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_response_header: Final = entity_reader(ResponseHeader)


@given(from_type(ResponseHeader))
@settings(max_examples=1)
def test_response_header_roundtrip(instance: ResponseHeader) -> None:
    writer = entity_writer(ResponseHeader)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_response_header(buffer)
    assert instance == result
