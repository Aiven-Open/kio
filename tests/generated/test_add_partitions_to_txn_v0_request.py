from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.add_partitions_to_txn.v0.request import AddPartitionsToTxnRequest
from kio.schema.add_partitions_to_txn.v0.request import AddPartitionsToTxnTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AddPartitionsToTxnTopic))
@settings(max_examples=1)
def test_add_partitions_to_txn_topic_roundtrip(
    instance: AddPartitionsToTxnTopic,
) -> None:
    writer = entity_writer(AddPartitionsToTxnTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AddPartitionsToTxnTopic))
    assert instance == result


@given(from_type(AddPartitionsToTxnRequest))
@settings(max_examples=1)
def test_add_partitions_to_txn_request_roundtrip(
    instance: AddPartitionsToTxnRequest,
) -> None:
    writer = entity_writer(AddPartitionsToTxnRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AddPartitionsToTxnRequest))
    assert instance == result
