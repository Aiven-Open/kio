from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.envelope.v0.request import EnvelopeRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_envelope_request: Final = entity_reader(EnvelopeRequest)


@given(from_type(EnvelopeRequest))
@settings(max_examples=1)
def test_envelope_request_roundtrip(instance: EnvelopeRequest) -> None:
    writer = entity_writer(EnvelopeRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_envelope_request(buffer)
    assert instance == result
