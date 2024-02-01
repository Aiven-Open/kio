from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.offset_delete.v0.request import OffsetDeleteRequest
from kio.schema.offset_delete.v0.request import OffsetDeleteRequestPartition
from kio.schema.offset_delete.v0.request import OffsetDeleteRequestTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_delete_request_partition: Final = entity_reader(
    OffsetDeleteRequestPartition
)


@pytest.mark.roundtrip
@given(from_type(OffsetDeleteRequestPartition))
def test_offset_delete_request_partition_roundtrip(
    instance: OffsetDeleteRequestPartition,
) -> None:
    writer = entity_writer(OffsetDeleteRequestPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_delete_request_partition(buffer)
    assert instance == result


read_offset_delete_request_topic: Final = entity_reader(OffsetDeleteRequestTopic)


@pytest.mark.roundtrip
@given(from_type(OffsetDeleteRequestTopic))
def test_offset_delete_request_topic_roundtrip(
    instance: OffsetDeleteRequestTopic,
) -> None:
    writer = entity_writer(OffsetDeleteRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_delete_request_topic(buffer)
    assert instance == result


read_offset_delete_request: Final = entity_reader(OffsetDeleteRequest)


@pytest.mark.roundtrip
@given(from_type(OffsetDeleteRequest))
def test_offset_delete_request_roundtrip(instance: OffsetDeleteRequest) -> None:
    writer = entity_writer(OffsetDeleteRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_delete_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(OffsetDeleteRequest))
def test_offset_delete_request_java(
    instance: OffsetDeleteRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
