from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_transactions.v0.request import ListTransactionsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_list_transactions_request: Final = entity_reader(ListTransactionsRequest)


@given(from_type(ListTransactionsRequest))
@settings(max_examples=1)
def test_list_transactions_request_roundtrip(instance: ListTransactionsRequest) -> None:
    writer = entity_writer(ListTransactionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_transactions_request(buffer)
    assert instance == result
