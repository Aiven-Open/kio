from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sasl_handshake.v1.response import SaslHandshakeResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_sasl_handshake_response: Final = entity_reader(SaslHandshakeResponse)


@given(from_type(SaslHandshakeResponse))
@settings(max_examples=1)
def test_sasl_handshake_response_roundtrip(instance: SaslHandshakeResponse) -> None:
    writer = entity_writer(SaslHandshakeResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sasl_handshake_response(buffer)
    assert instance == result
