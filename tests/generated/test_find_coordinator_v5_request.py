from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.find_coordinator.v5.request import FindCoordinatorRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_find_coordinator_request: Final = entity_reader(FindCoordinatorRequest)


@pytest.mark.roundtrip
@given(from_type(FindCoordinatorRequest))
def test_find_coordinator_request_roundtrip(instance: FindCoordinatorRequest) -> None:
    writer = entity_writer(FindCoordinatorRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_find_coordinator_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(FindCoordinatorRequest))
def test_find_coordinator_request_java(
    instance: FindCoordinatorRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
