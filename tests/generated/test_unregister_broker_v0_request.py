from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.unregister_broker.v0.request import UnregisterBrokerRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_unregister_broker_request: Final = entity_reader(UnregisterBrokerRequest)


@pytest.mark.roundtrip
@given(from_type(UnregisterBrokerRequest))
@settings(max_examples=1)
def test_unregister_broker_request_roundtrip(instance: UnregisterBrokerRequest) -> None:
    writer = entity_writer(UnregisterBrokerRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_unregister_broker_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UnregisterBrokerRequest))
def test_unregister_broker_request_java(
    instance: UnregisterBrokerRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
