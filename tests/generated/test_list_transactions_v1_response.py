from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_transactions.v1.response import ListTransactionsResponse
from kio.schema.list_transactions.v1.response import TransactionState
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_transaction_state: Final = entity_reader(TransactionState)


@pytest.mark.roundtrip
@given(from_type(TransactionState))
def test_transaction_state_roundtrip(instance: TransactionState) -> None:
    writer = entity_writer(TransactionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_transaction_state(buffer)
    assert instance == result


read_list_transactions_response: Final = entity_reader(ListTransactionsResponse)


@pytest.mark.roundtrip
@given(from_type(ListTransactionsResponse))
def test_list_transactions_response_roundtrip(
    instance: ListTransactionsResponse,
) -> None:
    writer = entity_writer(ListTransactionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_transactions_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListTransactionsResponse))
def test_list_transactions_response_java(
    instance: ListTransactionsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
