from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.unregister_controller.v0.response import UnregisterControllerResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_unregister_controller_response: Final = entity_reader(UnregisterControllerResponse)


@pytest.mark.roundtrip
@given(from_type(UnregisterControllerResponse))
def test_unregister_controller_response_roundtrip(
    instance: UnregisterControllerResponse,
) -> None:
    writer = entity_writer(UnregisterControllerResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_unregister_controller_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(UnregisterControllerResponse))
def test_unregister_controller_response_java(
    instance: UnregisterControllerResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
