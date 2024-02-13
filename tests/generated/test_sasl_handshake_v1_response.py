from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.sasl_handshake.v1.response import SaslHandshakeResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_sasl_handshake_response: Final = entity_reader(SaslHandshakeResponse)


@pytest.mark.roundtrip
@given(from_type(SaslHandshakeResponse))
def test_sasl_handshake_response_roundtrip(instance: SaslHandshakeResponse) -> None:
    writer = entity_writer(SaslHandshakeResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sasl_handshake_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(SaslHandshakeResponse))
def test_sasl_handshake_response_java(
    instance: SaslHandshakeResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
