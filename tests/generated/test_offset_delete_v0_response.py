from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_delete.v0.response import OffsetDeleteResponsePartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetDeleteResponsePartition))
@settings(max_examples=1)
def test_offset_delete_response_partition_roundtrip(
    instance: OffsetDeleteResponsePartition,
) -> None:
    writer = entity_writer(OffsetDeleteResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetDeleteResponsePartition))
    assert instance == result


from kio.schema.offset_delete.v0.response import OffsetDeleteResponseTopic


@given(from_type(OffsetDeleteResponseTopic))
@settings(max_examples=1)
def test_offset_delete_response_topic_roundtrip(
    instance: OffsetDeleteResponseTopic,
) -> None:
    writer = entity_writer(OffsetDeleteResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetDeleteResponseTopic))
    assert instance == result


from kio.schema.offset_delete.v0.response import OffsetDeleteResponse


@given(from_type(OffsetDeleteResponse))
@settings(max_examples=1)
def test_offset_delete_response_roundtrip(instance: OffsetDeleteResponse) -> None:
    writer = entity_writer(OffsetDeleteResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetDeleteResponse))
    assert instance == result
