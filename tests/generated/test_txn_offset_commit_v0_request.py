from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.txn_offset_commit.v0.request import TxnOffsetCommitRequest
from kio.schema.txn_offset_commit.v0.request import TxnOffsetCommitRequestPartition
from kio.schema.txn_offset_commit.v0.request import TxnOffsetCommitRequestTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(TxnOffsetCommitRequestPartition))
@settings(max_examples=1)
def test_txn_offset_commit_request_partition_roundtrip(
    instance: TxnOffsetCommitRequestPartition,
) -> None:
    writer = entity_writer(TxnOffsetCommitRequestPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TxnOffsetCommitRequestPartition))
    assert instance == result


@given(from_type(TxnOffsetCommitRequestTopic))
@settings(max_examples=1)
def test_txn_offset_commit_request_topic_roundtrip(
    instance: TxnOffsetCommitRequestTopic,
) -> None:
    writer = entity_writer(TxnOffsetCommitRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TxnOffsetCommitRequestTopic))
    assert instance == result


@given(from_type(TxnOffsetCommitRequest))
@settings(max_examples=1)
def test_txn_offset_commit_request_roundtrip(instance: TxnOffsetCommitRequest) -> None:
    writer = entity_writer(TxnOffsetCommitRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TxnOffsetCommitRequest))
    assert instance == result
