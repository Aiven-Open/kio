from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.allocate_producer_ids.v0.request import AllocateProducerIdsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_allocate_producer_ids_request: Final = entity_reader(AllocateProducerIdsRequest)


@pytest.mark.roundtrip
@given(from_type(AllocateProducerIdsRequest))
def test_allocate_producer_ids_request_roundtrip(
    instance: AllocateProducerIdsRequest,
) -> None:
    writer = entity_writer(AllocateProducerIdsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_allocate_producer_ids_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AllocateProducerIdsRequest))
def test_allocate_producer_ids_request_java(
    instance: AllocateProducerIdsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
