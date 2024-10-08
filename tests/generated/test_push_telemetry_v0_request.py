from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.push_telemetry.v0.request import PushTelemetryRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_push_telemetry_request: Final = entity_reader(PushTelemetryRequest)


@pytest.mark.roundtrip
@given(from_type(PushTelemetryRequest))
def test_push_telemetry_request_roundtrip(instance: PushTelemetryRequest) -> None:
    writer = entity_writer(PushTelemetryRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_push_telemetry_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(PushTelemetryRequest))
def test_push_telemetry_request_java(
    instance: PushTelemetryRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
