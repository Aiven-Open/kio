from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.controlled_shutdown.v1.request import ControlledShutdownRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_controlled_shutdown_request: Final = entity_reader(ControlledShutdownRequest)


@given(from_type(ControlledShutdownRequest))
@settings(max_examples=1)
def test_controlled_shutdown_request_roundtrip(
    instance: ControlledShutdownRequest,
) -> None:
    writer = entity_writer(ControlledShutdownRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_controlled_shutdown_request(buffer)
    assert instance == result


@given(instance=from_type(ControlledShutdownRequest))
def test_controlled_shutdown_request_java(
    instance: ControlledShutdownRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
