from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.allocate_producer_ids.v0.response import AllocateProducerIdsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_allocate_producer_ids_response: Final = entity_reader(AllocateProducerIdsResponse)


@given(from_type(AllocateProducerIdsResponse))
@settings(max_examples=1)
def test_allocate_producer_ids_response_roundtrip(
    instance: AllocateProducerIdsResponse,
) -> None:
    writer = entity_writer(AllocateProducerIdsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_allocate_producer_ids_response(buffer)
    assert instance == result


@given(instance=from_type(AllocateProducerIdsResponse))
def test_allocate_producer_ids_response_java(
    instance: AllocateProducerIdsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
