from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.end_txn.v0.response import EndTxnResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(EndTxnResponse))
@settings(max_examples=1)
def test_end_txn_response_roundtrip(instance: EndTxnResponse) -> None:
    writer = entity_writer(EndTxnResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EndTxnResponse))
    assert instance == result
