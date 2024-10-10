from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_topic_partitions.v0.request import Cursor
from kio.schema.describe_topic_partitions.v0.request import (
    DescribeTopicPartitionsRequest,
)
from kio.schema.describe_topic_partitions.v0.request import TopicRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_topic_request: Final = entity_reader(TopicRequest)


@pytest.mark.roundtrip
@given(from_type(TopicRequest))
def test_topic_request_roundtrip(instance: TopicRequest) -> None:
    writer = entity_writer(TopicRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_request(buffer)
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


read_describe_topic_partitions_request: Final = entity_reader(
    DescribeTopicPartitionsRequest
)


@pytest.mark.roundtrip
@given(from_type(DescribeTopicPartitionsRequest))
def test_describe_topic_partitions_request_roundtrip(
    instance: DescribeTopicPartitionsRequest,
) -> None:
    writer = entity_writer(DescribeTopicPartitionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_topic_partitions_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeTopicPartitionsRequest))
def test_describe_topic_partitions_request_java(
    instance: DescribeTopicPartitionsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
