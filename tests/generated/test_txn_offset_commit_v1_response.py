from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.txn_offset_commit.v1.response import TxnOffsetCommitResponse
from kio.schema.txn_offset_commit.v1.response import TxnOffsetCommitResponsePartition
from kio.schema.txn_offset_commit.v1.response import TxnOffsetCommitResponseTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(TxnOffsetCommitResponsePartition))
@settings(max_examples=1)
def test_txn_offset_commit_response_partition_roundtrip(
    instance: TxnOffsetCommitResponsePartition,
) -> None:
    writer = entity_writer(TxnOffsetCommitResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TxnOffsetCommitResponsePartition))
    assert instance == result


@given(from_type(TxnOffsetCommitResponseTopic))
@settings(max_examples=1)
def test_txn_offset_commit_response_topic_roundtrip(
    instance: TxnOffsetCommitResponseTopic,
) -> None:
    writer = entity_writer(TxnOffsetCommitResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TxnOffsetCommitResponseTopic))
    assert instance == result


@given(from_type(TxnOffsetCommitResponse))
@settings(max_examples=1)
def test_txn_offset_commit_response_roundtrip(
    instance: TxnOffsetCommitResponse,
) -> None:
    writer = entity_writer(TxnOffsetCommitResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TxnOffsetCommitResponse))
    assert instance == result
