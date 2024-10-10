from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_topic_partitions.v0.response import Cursor
from kio.schema.describe_topic_partitions.v0.response import (
    DescribeTopicPartitionsResponse,
)
from kio.schema.describe_topic_partitions.v0.response import (
    DescribeTopicPartitionsResponsePartition,
)
from kio.schema.describe_topic_partitions.v0.response import (
    DescribeTopicPartitionsResponseTopic,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_topic_partitions_response_partition: Final = entity_reader(
    DescribeTopicPartitionsResponsePartition
)


@pytest.mark.roundtrip
@given(from_type(DescribeTopicPartitionsResponsePartition))
def test_describe_topic_partitions_response_partition_roundtrip(
    instance: DescribeTopicPartitionsResponsePartition,
) -> None:
    writer = entity_writer(DescribeTopicPartitionsResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_topic_partitions_response_partition(buffer)
    assert instance == result


read_describe_topic_partitions_response_topic: Final = entity_reader(
    DescribeTopicPartitionsResponseTopic
)


@pytest.mark.roundtrip
@given(from_type(DescribeTopicPartitionsResponseTopic))
def test_describe_topic_partitions_response_topic_roundtrip(
    instance: DescribeTopicPartitionsResponseTopic,
) -> None:
    writer = entity_writer(DescribeTopicPartitionsResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_topic_partitions_response_topic(buffer)
    assert instance == result


read_cursor: Final = entity_reader(Cursor)


@pytest.mark.roundtrip
@given(from_type(Cursor))
def test_cursor_roundtrip(instance: Cursor) -> None:
    writer = entity_writer(Cursor)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_cursor(buffer)
    assert instance == result


read_describe_topic_partitions_response: Final = entity_reader(
    DescribeTopicPartitionsResponse
)


@pytest.mark.roundtrip
@given(from_type(DescribeTopicPartitionsResponse))
def test_describe_topic_partitions_response_roundtrip(
    instance: DescribeTopicPartitionsResponse,
) -> None:
    writer = entity_writer(DescribeTopicPartitionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_topic_partitions_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeTopicPartitionsResponse))
def test_describe_topic_partitions_response_java(
    instance: DescribeTopicPartitionsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
