from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.consumer_group_heartbeat.v0.request import Assignor
from kio.schema.consumer_group_heartbeat.v0.request import ConsumerGroupHeartbeatRequest
from kio.schema.consumer_group_heartbeat.v0.request import TopicPartitions
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_assignor: Final = entity_reader(Assignor)


@given(from_type(Assignor))
@settings(max_examples=1)
def test_assignor_roundtrip(instance: Assignor) -> None:
    writer = entity_writer(Assignor)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_assignor(buffer)
    assert instance == result


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


read_consumer_group_heartbeat_request: Final = entity_reader(
    ConsumerGroupHeartbeatRequest
)


@given(from_type(ConsumerGroupHeartbeatRequest))
@settings(max_examples=1)
def test_consumer_group_heartbeat_request_roundtrip(
    instance: ConsumerGroupHeartbeatRequest,
) -> None:
    writer = entity_writer(ConsumerGroupHeartbeatRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_consumer_group_heartbeat_request(buffer)
    assert instance == result


@given(instance=from_type(ConsumerGroupHeartbeatRequest))
def test_consumer_group_heartbeat_request_java(
    instance: ConsumerGroupHeartbeatRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
