from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_partition_reassignments.v0.response import (
    OngoingPartitionReassignment,
)
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OngoingPartitionReassignment))
@settings(max_examples=1)
def test_ongoing_partition_reassignment_roundtrip(
    instance: OngoingPartitionReassignment,
) -> None:
    writer = entity_writer(OngoingPartitionReassignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OngoingPartitionReassignment))
    assert instance == result


from kio.schema.list_partition_reassignments.v0.response import OngoingTopicReassignment


@given(from_type(OngoingTopicReassignment))
@settings(max_examples=1)
def test_ongoing_topic_reassignment_roundtrip(
    instance: OngoingTopicReassignment,
) -> None:
    writer = entity_writer(OngoingTopicReassignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OngoingTopicReassignment))
    assert instance == result


from kio.schema.list_partition_reassignments.v0.response import (
    ListPartitionReassignmentsResponse,
)


@given(from_type(ListPartitionReassignmentsResponse))
@settings(max_examples=1)
def test_list_partition_reassignments_response_roundtrip(
    instance: ListPartitionReassignmentsResponse,
) -> None:
    writer = entity_writer(ListPartitionReassignmentsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListPartitionReassignmentsResponse))
    assert instance == result
