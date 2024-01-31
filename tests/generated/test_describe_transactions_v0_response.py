from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_transactions.v0.response import DescribeTransactionsResponse
from kio.schema.describe_transactions.v0.response import TopicData
from kio.schema.describe_transactions.v0.response import TransactionState
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_topic_data: Final = entity_reader(TopicData)


@pytest.mark.roundtrip
@given(from_type(TopicData))
@settings(max_examples=1)
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_data(buffer)
    assert instance == result


read_transaction_state: Final = entity_reader(TransactionState)


@pytest.mark.roundtrip
@given(from_type(TransactionState))
@settings(max_examples=1)
def test_transaction_state_roundtrip(instance: TransactionState) -> None:
    writer = entity_writer(TransactionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_transaction_state(buffer)
    assert instance == result


read_describe_transactions_response: Final = entity_reader(DescribeTransactionsResponse)


@pytest.mark.roundtrip
@given(from_type(DescribeTransactionsResponse))
@settings(max_examples=1)
def test_describe_transactions_response_roundtrip(
    instance: DescribeTransactionsResponse,
) -> None:
    writer = entity_writer(DescribeTransactionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_transactions_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeTransactionsResponse))
def test_describe_transactions_response_java(
    instance: DescribeTransactionsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
