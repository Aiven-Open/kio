from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.end_txn.v1.request import EndTxnRequest
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(EndTxnRequest))
@settings(max_examples=1)
def test_end_txn_request_roundtrip(instance: EndTxnRequest) -> None:
    writer = entity_writer(EndTxnRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(EndTxnRequest))
    assert instance == result
