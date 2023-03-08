from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.fetch.v12.response import AbortedTransaction
from kio.schema.fetch.v12.response import EpochEndOffset
from kio.schema.fetch.v12.response import FetchableTopicResponse
from kio.schema.fetch.v12.response import FetchResponse
from kio.schema.fetch.v12.response import LeaderIdAndEpoch
from kio.schema.fetch.v12.response import PartitionData
from kio.schema.fetch.v12.response import SnapshotId
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(EpochEndOffset))
@settings(max_examples=1)
def test_epoch_end_offset_roundtrip(instance: EpochEndOffset) -> None:
    writer = entity_writer(EpochEndOffset)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EpochEndOffset))
    assert instance == result


@given(from_type(LeaderIdAndEpoch))
@settings(max_examples=1)
def test_leader_id_and_epoch_roundtrip(instance: LeaderIdAndEpoch) -> None:
    writer = entity_writer(LeaderIdAndEpoch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderIdAndEpoch))
    assert instance == result


@given(from_type(SnapshotId))
@settings(max_examples=1)
def test_snapshot_id_roundtrip(instance: SnapshotId) -> None:
    writer = entity_writer(SnapshotId)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(SnapshotId))
    assert instance == result


@given(from_type(AbortedTransaction))
@settings(max_examples=1)
def test_aborted_transaction_roundtrip(instance: AbortedTransaction) -> None:
    writer = entity_writer(AbortedTransaction)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AbortedTransaction))
    assert instance == result


@given(from_type(PartitionData))
@settings(max_examples=1)
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(PartitionData))
    assert instance == result


@given(from_type(FetchableTopicResponse))
@settings(max_examples=1)
def test_fetchable_topic_response_roundtrip(instance: FetchableTopicResponse) -> None:
    writer = entity_writer(FetchableTopicResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchableTopicResponse))
    assert instance == result


@given(from_type(FetchResponse))
@settings(max_examples=1)
def test_fetch_response_roundtrip(instance: FetchResponse) -> None:
    writer = entity_writer(FetchResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(FetchResponse))
    assert instance == result
