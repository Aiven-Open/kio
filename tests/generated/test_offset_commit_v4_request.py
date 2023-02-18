from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_commit.v4.request import OffsetCommitRequestPartition
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetCommitRequestPartition))
@settings(max_examples=1)
def test_offset_commit_request_partition_roundtrip(
    instance: OffsetCommitRequestPartition,
) -> None:
    writer = entity_writer(OffsetCommitRequestPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetCommitRequestPartition))
    assert instance == result


from kio.schema.offset_commit.v4.request import OffsetCommitRequestTopic


@given(from_type(OffsetCommitRequestTopic))
@settings(max_examples=1)
def test_offset_commit_request_topic_roundtrip(
    instance: OffsetCommitRequestTopic,
) -> None:
    writer = entity_writer(OffsetCommitRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetCommitRequestTopic))
    assert instance == result


from kio.schema.offset_commit.v4.request import OffsetCommitRequest


@given(from_type(OffsetCommitRequest))
@settings(max_examples=1)
def test_offset_commit_request_roundtrip(instance: OffsetCommitRequest) -> None:
    writer = entity_writer(OffsetCommitRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetCommitRequest))
    assert instance == result
