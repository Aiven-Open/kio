from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_offsets.v2.request import ListOffsetsPartition
from kio.schema.list_offsets.v2.request import ListOffsetsRequest
from kio.schema.list_offsets.v2.request import ListOffsetsTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ListOffsetsPartition))
@settings(max_examples=1)
def test_list_offsets_partition_roundtrip(instance: ListOffsetsPartition) -> None:
    writer = entity_writer(ListOffsetsPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListOffsetsPartition))
    assert instance == result


@given(from_type(ListOffsetsTopic))
@settings(max_examples=1)
def test_list_offsets_topic_roundtrip(instance: ListOffsetsTopic) -> None:
    writer = entity_writer(ListOffsetsTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListOffsetsTopic))
    assert instance == result


@given(from_type(ListOffsetsRequest))
@settings(max_examples=1)
def test_list_offsets_request_roundtrip(instance: ListOffsetsRequest) -> None:
    writer = entity_writer(ListOffsetsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListOffsetsRequest))
    assert instance == result
