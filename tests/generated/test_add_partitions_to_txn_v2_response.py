from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.add_partitions_to_txn.v2.response import (
    AddPartitionsToTxnPartitionResult,
)
from kio.schema.add_partitions_to_txn.v2.response import AddPartitionsToTxnResponse
from kio.schema.add_partitions_to_txn.v2.response import AddPartitionsToTxnTopicResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AddPartitionsToTxnPartitionResult))
@settings(max_examples=1)
def test_add_partitions_to_txn_partition_result_roundtrip(
    instance: AddPartitionsToTxnPartitionResult,
) -> None:
    writer = entity_writer(AddPartitionsToTxnPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AddPartitionsToTxnPartitionResult))
    assert instance == result


@given(from_type(AddPartitionsToTxnTopicResult))
@settings(max_examples=1)
def test_add_partitions_to_txn_topic_result_roundtrip(
    instance: AddPartitionsToTxnTopicResult,
) -> None:
    writer = entity_writer(AddPartitionsToTxnTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AddPartitionsToTxnTopicResult))
    assert instance == result


@given(from_type(AddPartitionsToTxnResponse))
@settings(max_examples=1)
def test_add_partitions_to_txn_response_roundtrip(
    instance: AddPartitionsToTxnResponse,
) -> None:
    writer = entity_writer(AddPartitionsToTxnResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AddPartitionsToTxnResponse))
    assert instance == result
