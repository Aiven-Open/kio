from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.envelope.v0.response import EnvelopeResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_envelope_response: Final = entity_reader(EnvelopeResponse)


@pytest.mark.roundtrip
@given(from_type(EnvelopeResponse))
def test_envelope_response_roundtrip(instance: EnvelopeResponse) -> None:
    writer = entity_writer(EnvelopeResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_envelope_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(EnvelopeResponse))
def test_envelope_response_java(
    instance: EnvelopeResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
