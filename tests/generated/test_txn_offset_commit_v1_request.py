from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.txn_offset_commit.v1.request import TxnOffsetCommitRequest
from kio.schema.txn_offset_commit.v1.request import TxnOffsetCommitRequestPartition
from kio.schema.txn_offset_commit.v1.request import TxnOffsetCommitRequestTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_txn_offset_commit_request_partition: Final = entity_reader(
    TxnOffsetCommitRequestPartition
)


@pytest.mark.roundtrip
@given(from_type(TxnOffsetCommitRequestPartition))
def test_txn_offset_commit_request_partition_roundtrip(
    instance: TxnOffsetCommitRequestPartition,
) -> None:
    writer = entity_writer(TxnOffsetCommitRequestPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_txn_offset_commit_request_partition(buffer)
    assert instance == result


read_txn_offset_commit_request_topic: Final = entity_reader(TxnOffsetCommitRequestTopic)


@pytest.mark.roundtrip
@given(from_type(TxnOffsetCommitRequestTopic))
def test_txn_offset_commit_request_topic_roundtrip(
    instance: TxnOffsetCommitRequestTopic,
) -> None:
    writer = entity_writer(TxnOffsetCommitRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_txn_offset_commit_request_topic(buffer)
    assert instance == result


read_txn_offset_commit_request: Final = entity_reader(TxnOffsetCommitRequest)


@pytest.mark.roundtrip
@given(from_type(TxnOffsetCommitRequest))
def test_txn_offset_commit_request_roundtrip(instance: TxnOffsetCommitRequest) -> None:
    writer = entity_writer(TxnOffsetCommitRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_txn_offset_commit_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(TxnOffsetCommitRequest))
def test_txn_offset_commit_request_java(
    instance: TxnOffsetCommitRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
