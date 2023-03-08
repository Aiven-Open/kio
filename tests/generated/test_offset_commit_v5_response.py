from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.offset_commit.v5.response import OffsetCommitResponse
from kio.schema.offset_commit.v5.response import OffsetCommitResponsePartition
from kio.schema.offset_commit.v5.response import OffsetCommitResponseTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(OffsetCommitResponsePartition))
@settings(max_examples=1)
def test_offset_commit_response_partition_roundtrip(
    instance: OffsetCommitResponsePartition,
) -> None:
    writer = entity_writer(OffsetCommitResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetCommitResponsePartition))
    assert instance == result


@given(from_type(OffsetCommitResponseTopic))
@settings(max_examples=1)
def test_offset_commit_response_topic_roundtrip(
    instance: OffsetCommitResponseTopic,
) -> None:
    writer = entity_writer(OffsetCommitResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetCommitResponseTopic))
    assert instance == result


@given(from_type(OffsetCommitResponse))
@settings(max_examples=1)
def test_offset_commit_response_roundtrip(instance: OffsetCommitResponse) -> None:
    writer = entity_writer(OffsetCommitResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(OffsetCommitResponse))
    assert instance == result
