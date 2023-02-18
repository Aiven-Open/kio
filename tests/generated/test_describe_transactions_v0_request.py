from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_transactions.v0.request import DescribeTransactionsRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DescribeTransactionsRequest))
@settings(max_examples=1)
def test_describe_transactions_request_roundtrip(
    instance: DescribeTransactionsRequest,
) -> None:
    writer = entity_writer(DescribeTransactionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DescribeTransactionsRequest))
    assert instance == result
