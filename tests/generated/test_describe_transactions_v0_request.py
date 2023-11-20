from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_transactions.v0.request import DescribeTransactionsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_transactions_request: Final = entity_reader(DescribeTransactionsRequest)


@pytest.mark.roundtrip
@given(from_type(DescribeTransactionsRequest))
@settings(max_examples=1)
def test_describe_transactions_request_roundtrip(
    instance: DescribeTransactionsRequest,
) -> None:
    writer = entity_writer(DescribeTransactionsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_transactions_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeTransactionsRequest))
def test_describe_transactions_request_java(
    instance: DescribeTransactionsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
