from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_partition_reassignments.v0.response import (
    ReassignablePartitionResponse,
)
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ReassignablePartitionResponse))
@settings(max_examples=1)
def test_reassignable_partition_response_roundtrip(
    instance: ReassignablePartitionResponse,
) -> None:
    writer = entity_writer(ReassignablePartitionResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ReassignablePartitionResponse))
    assert instance == result


from kio.schema.alter_partition_reassignments.v0.response import (
    ReassignableTopicResponse,
)


@given(from_type(ReassignableTopicResponse))
@settings(max_examples=1)
def test_reassignable_topic_response_roundtrip(
    instance: ReassignableTopicResponse,
) -> None:
    writer = entity_writer(ReassignableTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ReassignableTopicResponse))
    assert instance == result


from kio.schema.alter_partition_reassignments.v0.response import (
    AlterPartitionReassignmentsResponse,
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
        result = read_sync(buffer, entity_decoder(AlterPartitionReassignmentsResponse))
    assert instance == result
