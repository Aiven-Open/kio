from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_partition_reassignments.v0.request import (
    AlterPartitionReassignmentsRequest,
)
from kio.schema.alter_partition_reassignments.v0.request import ReassignablePartition
from kio.schema.alter_partition_reassignments.v0.request import ReassignableTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_reassignable_partition: Final = entity_reader(ReassignablePartition)


@given(from_type(ReassignablePartition))
@settings(max_examples=1)
def test_reassignable_partition_roundtrip(instance: ReassignablePartition) -> None:
    writer = entity_writer(ReassignablePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_reassignable_partition(buffer)
    assert instance == result


read_reassignable_topic: Final = entity_reader(ReassignableTopic)


@given(from_type(ReassignableTopic))
@settings(max_examples=1)
def test_reassignable_topic_roundtrip(instance: ReassignableTopic) -> None:
    writer = entity_writer(ReassignableTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_reassignable_topic(buffer)
    assert instance == result


read_alter_partition_reassignments_request: Final = entity_reader(
    AlterPartitionReassignmentsRequest
)


@given(from_type(AlterPartitionReassignmentsRequest))
@settings(max_examples=1)
def test_alter_partition_reassignments_request_roundtrip(
    instance: AlterPartitionReassignmentsRequest,
) -> None:
    writer = entity_writer(AlterPartitionReassignmentsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_partition_reassignments_request(buffer)
    assert instance == result


@given(instance=from_type(AlterPartitionReassignmentsRequest))
def test_alter_partition_reassignments_request_java(
    instance: AlterPartitionReassignmentsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
