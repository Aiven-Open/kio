from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.controller_registration.v0.response import (
    ControllerRegistrationResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_controller_registration_response: Final = entity_reader(
    ControllerRegistrationResponse
)


@pytest.mark.roundtrip
@given(from_type(ControllerRegistrationResponse))
def test_controller_registration_response_roundtrip(
    instance: ControllerRegistrationResponse,
) -> None:
    writer = entity_writer(ControllerRegistrationResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_controller_registration_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ControllerRegistrationResponse))
def test_controller_registration_response_java(
    instance: ControllerRegistrationResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
