from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.sasl_authenticate.v2.request import SaslAuthenticateRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_sasl_authenticate_request: Final = entity_reader(SaslAuthenticateRequest)


@pytest.mark.roundtrip
@given(from_type(SaslAuthenticateRequest))
def test_sasl_authenticate_request_roundtrip(instance: SaslAuthenticateRequest) -> None:
    writer = entity_writer(SaslAuthenticateRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sasl_authenticate_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(SaslAuthenticateRequest))
def test_sasl_authenticate_request_java(
    instance: SaslAuthenticateRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
