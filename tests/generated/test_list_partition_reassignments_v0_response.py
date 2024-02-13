from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_partition_reassignments.v0.response import (
    ListPartitionReassignmentsResponse,
)
from kio.schema.list_partition_reassignments.v0.response import (
    OngoingPartitionReassignment,
)
from kio.schema.list_partition_reassignments.v0.response import OngoingTopicReassignment
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_ongoing_partition_reassignment: Final = entity_reader(OngoingPartitionReassignment)


@pytest.mark.roundtrip
@given(from_type(OngoingPartitionReassignment))
def test_ongoing_partition_reassignment_roundtrip(
    instance: OngoingPartitionReassignment,
) -> None:
    writer = entity_writer(OngoingPartitionReassignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_ongoing_partition_reassignment(buffer)
    assert instance == result


read_ongoing_topic_reassignment: Final = entity_reader(OngoingTopicReassignment)


@pytest.mark.roundtrip
@given(from_type(OngoingTopicReassignment))
def test_ongoing_topic_reassignment_roundtrip(
    instance: OngoingTopicReassignment,
) -> None:
    writer = entity_writer(OngoingTopicReassignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_ongoing_topic_reassignment(buffer)
    assert instance == result


read_list_partition_reassignments_response: Final = entity_reader(
    ListPartitionReassignmentsResponse
)


@pytest.mark.roundtrip
@given(from_type(ListPartitionReassignmentsResponse))
def test_list_partition_reassignments_response_roundtrip(
    instance: ListPartitionReassignmentsResponse,
) -> None:
    writer = entity_writer(ListPartitionReassignmentsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_partition_reassignments_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListPartitionReassignmentsResponse))
def test_list_partition_reassignments_response_java(
    instance: ListPartitionReassignmentsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
