from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_transactions.v0.response import DescribeTransactionsResponse
from kio.schema.describe_transactions.v0.response import TopicData
from kio.schema.describe_transactions.v0.response import TransactionState
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(TopicData))
@settings(max_examples=1)
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TopicData))
    assert instance == result


@given(from_type(TransactionState))
@settings(max_examples=1)
def test_transaction_state_roundtrip(instance: TransactionState) -> None:
    writer = entity_writer(TransactionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TransactionState))
    assert instance == result


@given(from_type(DescribeTransactionsResponse))
@settings(max_examples=1)
def test_describe_transactions_response_roundtrip(
    instance: DescribeTransactionsResponse,
) -> None:
    writer = entity_writer(DescribeTransactionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeTransactionsResponse))
    assert instance == result
