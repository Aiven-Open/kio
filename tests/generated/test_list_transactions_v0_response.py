from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_transactions.v0.response import ListTransactionsResponse
from kio.schema.list_transactions.v0.response import TransactionState
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_transaction_state: Final = entity_reader(TransactionState)


@given(from_type(TransactionState))
@settings(max_examples=1)
def test_transaction_state_roundtrip(instance: TransactionState) -> None:
    writer = entity_writer(TransactionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_transaction_state(buffer)
    assert instance == result


read_list_transactions_response: Final = entity_reader(ListTransactionsResponse)


@given(from_type(ListTransactionsResponse))
@settings(max_examples=1)
def test_list_transactions_response_roundtrip(
    instance: ListTransactionsResponse,
) -> None:
    writer = entity_writer(ListTransactionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_transactions_response(buffer)
    assert instance == result
