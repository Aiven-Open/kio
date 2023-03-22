from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.add_offsets_to_txn.v0.request import AddOffsetsToTxnRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_add_offsets_to_txn_request: Final = entity_reader(AddOffsetsToTxnRequest)


@given(from_type(AddOffsetsToTxnRequest))
@settings(max_examples=1)
def test_add_offsets_to_txn_request_roundtrip(instance: AddOffsetsToTxnRequest) -> None:
    writer = entity_writer(AddOffsetsToTxnRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_offsets_to_txn_request(buffer)
    assert instance == result
