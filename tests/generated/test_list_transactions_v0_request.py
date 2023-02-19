from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.list_transactions.v0.request import ListTransactionsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(ListTransactionsRequest))
@settings(max_examples=1)
def test_list_transactions_request_roundtrip(instance: ListTransactionsRequest) -> None:
    writer = entity_writer(ListTransactionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(ListTransactionsRequest))
    assert instance == result
