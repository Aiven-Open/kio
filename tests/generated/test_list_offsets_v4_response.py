from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_offsets.v4.response import ListOffsetsPartitionResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ListOffsetsPartitionResponse))
@settings(max_examples=1)
def test_list_offsets_partition_response_roundtrip(
    instance: ListOffsetsPartitionResponse,
) -> None:
    writer = entity_writer(ListOffsetsPartitionResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListOffsetsPartitionResponse))
    assert instance == result


from kio.schema.list_offsets.v4.response import ListOffsetsTopicResponse


@given(from_type(ListOffsetsTopicResponse))
@settings(max_examples=1)
def test_list_offsets_topic_response_roundtrip(
    instance: ListOffsetsTopicResponse,
) -> None:
    writer = entity_writer(ListOffsetsTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListOffsetsTopicResponse))
    assert instance == result


from kio.schema.list_offsets.v4.response import ListOffsetsResponse


@given(from_type(ListOffsetsResponse))
@settings(max_examples=1)
def test_list_offsets_response_roundtrip(instance: ListOffsetsResponse) -> None:
    writer = entity_writer(ListOffsetsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListOffsetsResponse))
    assert instance == result
