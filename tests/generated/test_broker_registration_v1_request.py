from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.broker_registration.v1.request import BrokerRegistrationRequest
from kio.schema.broker_registration.v1.request import Feature
from kio.schema.broker_registration.v1.request import Listener
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_listener: Final = entity_reader(Listener)


@pytest.mark.roundtrip
@given(from_type(Listener))
@settings(max_examples=1)
def test_listener_roundtrip(instance: Listener) -> None:
    writer = entity_writer(Listener)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_listener(buffer)
    assert instance == result


read_feature: Final = entity_reader(Feature)


@pytest.mark.roundtrip
@given(from_type(Feature))
@settings(max_examples=1)
def test_feature_roundtrip(instance: Feature) -> None:
    writer = entity_writer(Feature)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_feature(buffer)
    assert instance == result


read_broker_registration_request: Final = entity_reader(BrokerRegistrationRequest)


@pytest.mark.roundtrip
@given(from_type(BrokerRegistrationRequest))
@settings(max_examples=1)
def test_broker_registration_request_roundtrip(
    instance: BrokerRegistrationRequest,
) -> None:
    writer = entity_writer(BrokerRegistrationRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_broker_registration_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(BrokerRegistrationRequest))
def test_broker_registration_request_java(
    instance: BrokerRegistrationRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
