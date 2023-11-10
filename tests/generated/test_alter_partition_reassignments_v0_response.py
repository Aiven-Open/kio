from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_partition_reassignments.v0.response import (
    AlterPartitionReassignmentsResponse,
)
from kio.schema.alter_partition_reassignments.v0.response import (
    ReassignablePartitionResponse,
)
from kio.schema.alter_partition_reassignments.v0.response import (
    ReassignableTopicResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_reassignable_partition_response: Final = entity_reader(
    ReassignablePartitionResponse
)


@given(from_type(ReassignablePartitionResponse))
@settings(max_examples=1)
def test_reassignable_partition_response_roundtrip(
    instance: ReassignablePartitionResponse,
) -> None:
    writer = entity_writer(ReassignablePartitionResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_reassignable_partition_response(buffer)
    assert instance == result


read_reassignable_topic_response: Final = entity_reader(ReassignableTopicResponse)


@given(from_type(ReassignableTopicResponse))
@settings(max_examples=1)
def test_reassignable_topic_response_roundtrip(
    instance: ReassignableTopicResponse,
) -> None:
    writer = entity_writer(ReassignableTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_reassignable_topic_response(buffer)
    assert instance == result


read_alter_partition_reassignments_response: Final = entity_reader(
    AlterPartitionReassignmentsResponse
)


@given(from_type(AlterPartitionReassignmentsResponse))
@settings(max_examples=1)
def test_alter_partition_reassignments_response_roundtrip(
    instance: AlterPartitionReassignmentsResponse,
) -> None:
    writer = entity_writer(AlterPartitionReassignmentsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_partition_reassignments_response(buffer)
    assert instance == result


@given(instance=from_type(AlterPartitionReassignmentsResponse))
def test_alter_partition_reassignments_response_java(
    instance: AlterPartitionReassignmentsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
