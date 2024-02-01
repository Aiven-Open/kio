from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.consumer_group_heartbeat.v0.response import Assignment
from kio.schema.consumer_group_heartbeat.v0.response import (
    ConsumerGroupHeartbeatResponse,
)
from kio.schema.consumer_group_heartbeat.v0.response import TopicPartitions
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_topic_partitions: Final = entity_reader(TopicPartitions)


@pytest.mark.roundtrip
@given(from_type(TopicPartitions))
@settings(max_examples=1)
def test_topic_partitions_roundtrip(instance: TopicPartitions) -> None:
    writer = entity_writer(TopicPartitions)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_partitions(buffer)
    assert instance == result


read_assignment: Final = entity_reader(Assignment)


@pytest.mark.roundtrip
@given(from_type(Assignment))
@settings(max_examples=1)
def test_assignment_roundtrip(instance: Assignment) -> None:
    writer = entity_writer(Assignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_assignment(buffer)
    assert instance == result


read_consumer_group_heartbeat_response: Final = entity_reader(
    ConsumerGroupHeartbeatResponse
)


@pytest.mark.roundtrip
@given(from_type(ConsumerGroupHeartbeatResponse))
@settings(max_examples=1)
def test_consumer_group_heartbeat_response_roundtrip(
    instance: ConsumerGroupHeartbeatResponse,
) -> None:
    writer = entity_writer(ConsumerGroupHeartbeatResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_consumer_group_heartbeat_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ConsumerGroupHeartbeatResponse))
def test_consumer_group_heartbeat_response_java(
    instance: ConsumerGroupHeartbeatResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
