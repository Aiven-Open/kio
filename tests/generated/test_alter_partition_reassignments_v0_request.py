from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_partition_reassignments.v0.request import (
    AlterPartitionReassignmentsRequest,
)
from kio.schema.alter_partition_reassignments.v0.request import ReassignablePartition
from kio.schema.alter_partition_reassignments.v0.request import ReassignableTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ReassignablePartition))
@settings(max_examples=1)
def test_reassignable_partition_roundtrip(instance: ReassignablePartition) -> None:
    writer = entity_writer(ReassignablePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ReassignablePartition))
    assert instance == result


@given(from_type(ReassignableTopic))
@settings(max_examples=1)
def test_reassignable_topic_roundtrip(instance: ReassignableTopic) -> None:
    writer = entity_writer(ReassignableTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ReassignableTopic))
    assert instance == result


@given(from_type(AlterPartitionReassignmentsRequest))
@settings(max_examples=1)
def test_alter_partition_reassignments_request_roundtrip(
    instance: AlterPartitionReassignmentsRequest,
) -> None:
    writer = entity_writer(AlterPartitionReassignmentsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterPartitionReassignmentsRequest))
    assert instance == result
