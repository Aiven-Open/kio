from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.add_offsets_to_txn.v2.response import AddOffsetsToTxnResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_add_offsets_to_txn_response: Final = entity_reader(AddOffsetsToTxnResponse)


@pytest.mark.roundtrip
@given(from_type(AddOffsetsToTxnResponse))
@settings(max_examples=1)
def test_add_offsets_to_txn_response_roundtrip(
    instance: AddOffsetsToTxnResponse,
) -> None:
    writer = entity_writer(AddOffsetsToTxnResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_offsets_to_txn_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AddOffsetsToTxnResponse))
def test_add_offsets_to_txn_response_java(
    instance: AddOffsetsToTxnResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
