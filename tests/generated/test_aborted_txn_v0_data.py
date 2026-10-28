from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.aborted_txn.v0.data import AbortedTxn
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_aborted_txn: Final = entity_reader(AbortedTxn)


@pytest.mark.roundtrip
@given(from_type(AbortedTxn))
def test_aborted_txn_roundtrip(instance: AbortedTxn) -> None:
    writer = entity_writer(AbortedTxn)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_aborted_txn(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(AbortedTxn))
def test_aborted_txn_java(instance: AbortedTxn, java_tester: JavaTester) -> None:
    java_tester.test(instance)
