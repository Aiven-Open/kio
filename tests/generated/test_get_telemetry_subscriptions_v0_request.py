from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.get_telemetry_subscriptions.v0.request import (
    GetTelemetrySubscriptionsRequest,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_get_telemetry_subscriptions_request: Final = entity_reader(
    GetTelemetrySubscriptionsRequest
)


@pytest.mark.roundtrip
@given(from_type(GetTelemetrySubscriptionsRequest))
def test_get_telemetry_subscriptions_request_roundtrip(
    instance: GetTelemetrySubscriptionsRequest,
) -> None:
    writer = entity_writer(GetTelemetrySubscriptionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_get_telemetry_subscriptions_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(GetTelemetrySubscriptionsRequest))
def test_get_telemetry_subscriptions_request_java(
    instance: GetTelemetrySubscriptionsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
