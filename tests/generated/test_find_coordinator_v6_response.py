from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.find_coordinator.v6.response import Coordinator
from kio.schema.find_coordinator.v6.response import FindCoordinatorResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_coordinator: Final = entity_reader(Coordinator)


@pytest.mark.roundtrip
@given(from_type(Coordinator))
def test_coordinator_roundtrip(instance: Coordinator) -> None:
    writer = entity_writer(Coordinator)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_coordinator(buffer)
    assert instance == result


read_find_coordinator_response: Final = entity_reader(FindCoordinatorResponse)


@pytest.mark.roundtrip
@given(from_type(FindCoordinatorResponse))
def test_find_coordinator_response_roundtrip(instance: FindCoordinatorResponse) -> None:
    writer = entity_writer(FindCoordinatorResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_find_coordinator_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(FindCoordinatorResponse))
def test_find_coordinator_response_java(
    instance: FindCoordinatorResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
