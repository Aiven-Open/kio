from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_transactions.v0.response import TransactionState
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(TransactionState))
@settings(max_examples=1)
def test_transaction_state_roundtrip(instance: TransactionState) -> None:
    writer = entity_writer(TransactionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(TransactionState))
    assert instance == result


from kio.schema.list_transactions.v0.response import ListTransactionsResponse


@given(from_type(ListTransactionsResponse))
@settings(max_examples=1)
def test_list_transactions_response_roundtrip(
    instance: ListTransactionsResponse,
) -> None:
    writer = entity_writer(ListTransactionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListTransactionsResponse))
    assert instance == result
