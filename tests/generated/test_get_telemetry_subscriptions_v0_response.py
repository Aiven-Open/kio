from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.get_telemetry_subscriptions.v0.response import (
    GetTelemetrySubscriptionsResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_get_telemetry_subscriptions_response: Final = entity_reader(
    GetTelemetrySubscriptionsResponse
)


@pytest.mark.roundtrip
@given(from_type(GetTelemetrySubscriptionsResponse))
def test_get_telemetry_subscriptions_response_roundtrip(
    instance: GetTelemetrySubscriptionsResponse,
) -> None:
    writer = entity_writer(GetTelemetrySubscriptionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_get_telemetry_subscriptions_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(GetTelemetrySubscriptionsResponse))
def test_get_telemetry_subscriptions_response_java(
    instance: GetTelemetrySubscriptionsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
