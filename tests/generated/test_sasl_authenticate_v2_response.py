from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.sasl_authenticate.v2.response import SaslAuthenticateResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_sasl_authenticate_response: Final = entity_reader(SaslAuthenticateResponse)


@pytest.mark.roundtrip
@given(from_type(SaslAuthenticateResponse))
@settings(max_examples=1)
def test_sasl_authenticate_response_roundtrip(
    instance: SaslAuthenticateResponse,
) -> None:
    writer = entity_writer(SaslAuthenticateResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sasl_authenticate_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(SaslAuthenticateResponse))
def test_sasl_authenticate_response_java(
    instance: SaslAuthenticateResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
