from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_partitions.v2.request import CreatePartitionsAssignment
from kio.schema.create_partitions.v2.request import CreatePartitionsRequest
from kio.schema.create_partitions.v2.request import CreatePartitionsTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(CreatePartitionsAssignment))
@settings(max_examples=1)
def test_create_partitions_assignment_roundtrip(
    instance: CreatePartitionsAssignment,
) -> None:
    writer = entity_writer(CreatePartitionsAssignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatePartitionsAssignment))
    assert instance == result


@given(from_type(CreatePartitionsTopic))
@settings(max_examples=1)
def test_create_partitions_topic_roundtrip(instance: CreatePartitionsTopic) -> None:
    writer = entity_writer(CreatePartitionsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatePartitionsTopic))
    assert instance == result


@given(from_type(CreatePartitionsRequest))
@settings(max_examples=1)
def test_create_partitions_request_roundtrip(instance: CreatePartitionsRequest) -> None:
    writer = entity_writer(CreatePartitionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatePartitionsRequest))
    assert instance == result
