from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.add_partitions_to_txn.v4.response import (
    AddPartitionsToTxnPartitionResult,
)
from kio.schema.add_partitions_to_txn.v4.response import AddPartitionsToTxnResponse
from kio.schema.add_partitions_to_txn.v4.response import AddPartitionsToTxnResult
from kio.schema.add_partitions_to_txn.v4.response import AddPartitionsToTxnTopicResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_add_partitions_to_txn_partition_result: Final = entity_reader(
    AddPartitionsToTxnPartitionResult
)


@pytest.mark.roundtrip
@given(from_type(AddPartitionsToTxnPartitionResult))
@settings(max_examples=1)
def test_add_partitions_to_txn_partition_result_roundtrip(
    instance: AddPartitionsToTxnPartitionResult,
) -> None:
    writer = entity_writer(AddPartitionsToTxnPartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_partitions_to_txn_partition_result(buffer)
    assert instance == result


read_add_partitions_to_txn_topic_result: Final = entity_reader(
    AddPartitionsToTxnTopicResult
)


@pytest.mark.roundtrip
@given(from_type(AddPartitionsToTxnTopicResult))
@settings(max_examples=1)
def test_add_partitions_to_txn_topic_result_roundtrip(
    instance: AddPartitionsToTxnTopicResult,
) -> None:
    writer = entity_writer(AddPartitionsToTxnTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_partitions_to_txn_topic_result(buffer)
    assert instance == result


read_add_partitions_to_txn_result: Final = entity_reader(AddPartitionsToTxnResult)


@pytest.mark.roundtrip
@given(from_type(AddPartitionsToTxnResult))
@settings(max_examples=1)
def test_add_partitions_to_txn_result_roundtrip(
    instance: AddPartitionsToTxnResult,
) -> None:
    writer = entity_writer(AddPartitionsToTxnResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_partitions_to_txn_result(buffer)
    assert instance == result


read_add_partitions_to_txn_response: Final = entity_reader(AddPartitionsToTxnResponse)


@pytest.mark.roundtrip
@given(from_type(AddPartitionsToTxnResponse))
@settings(max_examples=1)
def test_add_partitions_to_txn_response_roundtrip(
    instance: AddPartitionsToTxnResponse,
) -> None:
    writer = entity_writer(AddPartitionsToTxnResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_partitions_to_txn_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AddPartitionsToTxnResponse))
def test_add_partitions_to_txn_response_java(
    instance: AddPartitionsToTxnResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
