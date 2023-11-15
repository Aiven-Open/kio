from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.add_partitions_to_txn.v3.request import AddPartitionsToTxnRequest
from kio.schema.add_partitions_to_txn.v3.request import AddPartitionsToTxnTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_add_partitions_to_txn_topic: Final = entity_reader(AddPartitionsToTxnTopic)


@pytest.mark.roundtrip
@given(from_type(AddPartitionsToTxnTopic))
@settings(max_examples=1)
def test_add_partitions_to_txn_topic_roundtrip(
    instance: AddPartitionsToTxnTopic,
) -> None:
    writer = entity_writer(AddPartitionsToTxnTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_partitions_to_txn_topic(buffer)
    assert instance == result


read_add_partitions_to_txn_request: Final = entity_reader(AddPartitionsToTxnRequest)


@pytest.mark.roundtrip
@given(from_type(AddPartitionsToTxnRequest))
@settings(max_examples=1)
def test_add_partitions_to_txn_request_roundtrip(
    instance: AddPartitionsToTxnRequest,
) -> None:
    writer = entity_writer(AddPartitionsToTxnRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_partitions_to_txn_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AddPartitionsToTxnRequest))
def test_add_partitions_to_txn_request_java(
    instance: AddPartitionsToTxnRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
