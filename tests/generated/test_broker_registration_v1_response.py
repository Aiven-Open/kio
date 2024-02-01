from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.broker_registration.v1.response import BrokerRegistrationResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_broker_registration_response: Final = entity_reader(BrokerRegistrationResponse)


@pytest.mark.roundtrip
@given(from_type(BrokerRegistrationResponse))
@settings(max_examples=1)
def test_broker_registration_response_roundtrip(
    instance: BrokerRegistrationResponse,
) -> None:
    writer = entity_writer(BrokerRegistrationResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_broker_registration_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(BrokerRegistrationResponse))
def test_broker_registration_response_java(
    instance: BrokerRegistrationResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
