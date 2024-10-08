from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.push_telemetry.v0.response import PushTelemetryResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_push_telemetry_response: Final = entity_reader(PushTelemetryResponse)


@pytest.mark.roundtrip
@given(from_type(PushTelemetryResponse))
def test_push_telemetry_response_roundtrip(instance: PushTelemetryResponse) -> None:
    writer = entity_writer(PushTelemetryResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_push_telemetry_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(PushTelemetryResponse))
def test_push_telemetry_response_java(
    instance: PushTelemetryResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
