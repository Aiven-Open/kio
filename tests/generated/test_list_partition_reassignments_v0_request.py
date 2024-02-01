from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_partition_reassignments.v0.request import (
    ListPartitionReassignmentsRequest,
)
from kio.schema.list_partition_reassignments.v0.request import (
    ListPartitionReassignmentsTopics,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_list_partition_reassignments_topics: Final = entity_reader(
    ListPartitionReassignmentsTopics
)


@pytest.mark.roundtrip
@given(from_type(ListPartitionReassignmentsTopics))
def test_list_partition_reassignments_topics_roundtrip(
    instance: ListPartitionReassignmentsTopics,
) -> None:
    writer = entity_writer(ListPartitionReassignmentsTopics)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_partition_reassignments_topics(buffer)
    assert instance == result


read_list_partition_reassignments_request: Final = entity_reader(
    ListPartitionReassignmentsRequest
)


@pytest.mark.roundtrip
@given(from_type(ListPartitionReassignmentsRequest))
def test_list_partition_reassignments_request_roundtrip(
    instance: ListPartitionReassignmentsRequest,
) -> None:
    writer = entity_writer(ListPartitionReassignmentsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_partition_reassignments_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListPartitionReassignmentsRequest))
def test_list_partition_reassignments_request_java(
    instance: ListPartitionReassignmentsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
