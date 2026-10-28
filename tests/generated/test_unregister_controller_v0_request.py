from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.unregister_controller.v0.request import UnregisterControllerRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_unregister_controller_request: Final = entity_reader(UnregisterControllerRequest)


@pytest.mark.roundtrip
@given(from_type(UnregisterControllerRequest))
def test_unregister_controller_request_roundtrip(
    instance: UnregisterControllerRequest,
) -> None:
    writer = entity_writer(UnregisterControllerRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_unregister_controller_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(UnregisterControllerRequest))
def test_unregister_controller_request_java(
    instance: UnregisterControllerRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
