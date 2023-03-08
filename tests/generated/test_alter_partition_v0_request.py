from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_partition.v0.request import AlterPartitionRequest
from kio.schema.alter_partition.v0.request import PartitionData
from kio.schema.alter_partition.v0.request import TopicData
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(PartitionData))
@settings(max_examples=1)
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionData))
    assert instance == result


@given(from_type(TopicData))
@settings(max_examples=1)
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicData))
    assert instance == result


@given(from_type(AlterPartitionRequest))
@settings(max_examples=1)
def test_alter_partition_request_roundtrip(instance: AlterPartitionRequest) -> None:
    writer = entity_writer(AlterPartitionRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterPartitionRequest))
    assert instance == result
