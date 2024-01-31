from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_offsets.v6.response import ListOffsetsPartitionResponse
from kio.schema.list_offsets.v6.response import ListOffsetsResponse
from kio.schema.list_offsets.v6.response import ListOffsetsTopicResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_list_offsets_partition_response: Final = entity_reader(
    ListOffsetsPartitionResponse
)


@pytest.mark.roundtrip
@given(from_type(ListOffsetsPartitionResponse))
@settings(max_examples=1)
def test_list_offsets_partition_response_roundtrip(
    instance: ListOffsetsPartitionResponse,
) -> None:
    writer = entity_writer(ListOffsetsPartitionResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_offsets_partition_response(buffer)
    assert instance == result


read_list_offsets_topic_response: Final = entity_reader(ListOffsetsTopicResponse)


@pytest.mark.roundtrip
@given(from_type(ListOffsetsTopicResponse))
@settings(max_examples=1)
def test_list_offsets_topic_response_roundtrip(
    instance: ListOffsetsTopicResponse,
) -> None:
    writer = entity_writer(ListOffsetsTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_offsets_topic_response(buffer)
    assert instance == result


read_list_offsets_response: Final = entity_reader(ListOffsetsResponse)


@pytest.mark.roundtrip
@given(from_type(ListOffsetsResponse))
@settings(max_examples=1)
def test_list_offsets_response_roundtrip(instance: ListOffsetsResponse) -> None:
    writer = entity_writer(ListOffsetsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_offsets_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListOffsetsResponse))
def test_list_offsets_response_java(
    instance: ListOffsetsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
