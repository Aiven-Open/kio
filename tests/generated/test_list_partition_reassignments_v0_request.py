from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_partition_reassignments.v0.request import (
    ListPartitionReassignmentsTopics,
)
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ListPartitionReassignmentsTopics))
@settings(max_examples=1)
def test_list_partition_reassignments_topics_roundtrip(
    instance: ListPartitionReassignmentsTopics,
) -> None:
    writer = entity_writer(ListPartitionReassignmentsTopics)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListPartitionReassignmentsTopics))
    assert instance == result


from kio.schema.list_partition_reassignments.v0.request import (
    ListPartitionReassignmentsRequest,
)


@given(from_type(ListPartitionReassignmentsRequest))
@settings(max_examples=1)
def test_list_partition_reassignments_request_roundtrip(
    instance: ListPartitionReassignmentsRequest,
) -> None:
    writer = entity_writer(ListPartitionReassignmentsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListPartitionReassignmentsRequest))
    assert instance == result
