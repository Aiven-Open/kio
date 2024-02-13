from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_offsets.v2.request import ListOffsetsPartition
from kio.schema.list_offsets.v2.request import ListOffsetsRequest
from kio.schema.list_offsets.v2.request import ListOffsetsTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_list_offsets_partition: Final = entity_reader(ListOffsetsPartition)


@pytest.mark.roundtrip
@given(from_type(ListOffsetsPartition))
def test_list_offsets_partition_roundtrip(instance: ListOffsetsPartition) -> None:
    writer = entity_writer(ListOffsetsPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_offsets_partition(buffer)
    assert instance == result


read_list_offsets_topic: Final = entity_reader(ListOffsetsTopic)


@pytest.mark.roundtrip
@given(from_type(ListOffsetsTopic))
def test_list_offsets_topic_roundtrip(instance: ListOffsetsTopic) -> None:
    writer = entity_writer(ListOffsetsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_offsets_topic(buffer)
    assert instance == result


read_list_offsets_request: Final = entity_reader(ListOffsetsRequest)


@pytest.mark.roundtrip
@given(from_type(ListOffsetsRequest))
def test_list_offsets_request_roundtrip(instance: ListOffsetsRequest) -> None:
    writer = entity_writer(ListOffsetsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_offsets_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListOffsetsRequest))
def test_list_offsets_request_java(
    instance: ListOffsetsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
