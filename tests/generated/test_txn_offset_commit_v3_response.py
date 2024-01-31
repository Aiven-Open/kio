from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.txn_offset_commit.v3.response import TxnOffsetCommitResponse
from kio.schema.txn_offset_commit.v3.response import TxnOffsetCommitResponsePartition
from kio.schema.txn_offset_commit.v3.response import TxnOffsetCommitResponseTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_txn_offset_commit_response_partition: Final = entity_reader(
    TxnOffsetCommitResponsePartition
)


@pytest.mark.roundtrip
@given(from_type(TxnOffsetCommitResponsePartition))
@settings(max_examples=1)
def test_txn_offset_commit_response_partition_roundtrip(
    instance: TxnOffsetCommitResponsePartition,
) -> None:
    writer = entity_writer(TxnOffsetCommitResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_txn_offset_commit_response_partition(buffer)
    assert instance == result


read_txn_offset_commit_response_topic: Final = entity_reader(
    TxnOffsetCommitResponseTopic
)


@pytest.mark.roundtrip
@given(from_type(TxnOffsetCommitResponseTopic))
@settings(max_examples=1)
def test_txn_offset_commit_response_topic_roundtrip(
    instance: TxnOffsetCommitResponseTopic,
) -> None:
    writer = entity_writer(TxnOffsetCommitResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_txn_offset_commit_response_topic(buffer)
    assert instance == result


read_txn_offset_commit_response: Final = entity_reader(TxnOffsetCommitResponse)


@pytest.mark.roundtrip
@given(from_type(TxnOffsetCommitResponse))
@settings(max_examples=1)
def test_txn_offset_commit_response_roundtrip(
    instance: TxnOffsetCommitResponse,
) -> None:
    writer = entity_writer(TxnOffsetCommitResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_txn_offset_commit_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(TxnOffsetCommitResponse))
def test_txn_offset_commit_response_java(
    instance: TxnOffsetCommitResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
