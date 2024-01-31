from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sasl_handshake.v1.request import SaslHandshakeRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_sasl_handshake_request: Final = entity_reader(SaslHandshakeRequest)


@pytest.mark.roundtrip
@given(from_type(SaslHandshakeRequest))
@settings(max_examples=1)
def test_sasl_handshake_request_roundtrip(instance: SaslHandshakeRequest) -> None:
    writer = entity_writer(SaslHandshakeRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sasl_handshake_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(SaslHandshakeRequest))
def test_sasl_handshake_request_java(
    instance: SaslHandshakeRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
