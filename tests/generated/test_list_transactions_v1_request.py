from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_transactions.v1.request import ListTransactionsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_list_transactions_request: Final = entity_reader(ListTransactionsRequest)


@pytest.mark.roundtrip
@given(from_type(ListTransactionsRequest))
def test_list_transactions_request_roundtrip(instance: ListTransactionsRequest) -> None:
    writer = entity_writer(ListTransactionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_list_transactions_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListTransactionsRequest))
def test_list_transactions_request_java(
    instance: ListTransactionsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
