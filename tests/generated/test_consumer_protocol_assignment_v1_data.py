from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.consumer_protocol_assignment.v1.data import ConsumerProtocolAssignment
from kio.schema.consumer_protocol_assignment.v1.data import TopicPartition
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_topic_partition: Final = entity_reader(TopicPartition)


@given(from_type(TopicPartition))
@settings(max_examples=1)
def test_topic_partition_roundtrip(instance: TopicPartition) -> None:
    writer = entity_writer(TopicPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_partition(buffer)
    assert instance == result


read_consumer_protocol_assignment: Final = entity_reader(ConsumerProtocolAssignment)


@given(from_type(ConsumerProtocolAssignment))
@settings(max_examples=1)
def test_consumer_protocol_assignment_roundtrip(
    instance: ConsumerProtocolAssignment,
) -> None:
    writer = entity_writer(ConsumerProtocolAssignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_consumer_protocol_assignment(buffer)
    assert instance == result


@given(instance=from_type(ConsumerProtocolAssignment))
def test_consumer_protocol_assignment_java(
    instance: ConsumerProtocolAssignment, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
