from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.end_txn_marker.v0.data import EndTxnMarker
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_end_txn_marker: Final = entity_reader(EndTxnMarker)


@pytest.mark.roundtrip
@given(from_type(EndTxnMarker))
def test_end_txn_marker_roundtrip(instance: EndTxnMarker) -> None:
    writer = entity_writer(EndTxnMarker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_end_txn_marker(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(EndTxnMarker))
def test_end_txn_marker_java(instance: EndTxnMarker, java_tester: JavaTester) -> None:
    java_tester.test(instance)
