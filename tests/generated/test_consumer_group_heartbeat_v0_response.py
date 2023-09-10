from __future__ import annotations

from typing import Final

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
from tests.conftest import setup_buffer

read_topic_partitions: Final = entity_reader(TopicPartitions)


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
