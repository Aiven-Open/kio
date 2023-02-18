from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.add_offsets_to_txn.v2.response import AddOffsetsToTxnResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AddOffsetsToTxnResponse))
@settings(max_examples=1)
def test_add_offsets_to_txn_response_roundtrip(
    instance: AddOffsetsToTxnResponse,
) -> None:
    writer = entity_writer(AddOffsetsToTxnResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AddOffsetsToTxnResponse))
    assert instance == result
