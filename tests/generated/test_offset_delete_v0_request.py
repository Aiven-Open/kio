from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_delete.v0.request import OffsetDeleteRequestPartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetDeleteRequestPartition))
@settings(max_examples=1)
def test_offset_delete_request_partition_roundtrip(
    instance: OffsetDeleteRequestPartition,
) -> None:
    writer = entity_writer(OffsetDeleteRequestPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetDeleteRequestPartition))
    assert instance == result


from kio.schema.offset_delete.v0.request import OffsetDeleteRequestTopic


@given(from_type(OffsetDeleteRequestTopic))
@settings(max_examples=1)
def test_offset_delete_request_topic_roundtrip(
    instance: OffsetDeleteRequestTopic,
) -> None:
    writer = entity_writer(OffsetDeleteRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetDeleteRequestTopic))
    assert instance == result


from kio.schema.offset_delete.v0.request import OffsetDeleteRequest


@given(from_type(OffsetDeleteRequest))
@settings(max_examples=1)
def test_offset_delete_request_roundtrip(instance: OffsetDeleteRequest) -> None:
    writer = entity_writer(OffsetDeleteRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetDeleteRequest))
    assert instance == result
