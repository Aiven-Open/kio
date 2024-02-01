from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.offset_commit.v6.request import OffsetCommitRequest
from kio.schema.offset_commit.v6.request import OffsetCommitRequestPartition
from kio.schema.offset_commit.v6.request import OffsetCommitRequestTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_commit_request_partition: Final = entity_reader(
    OffsetCommitRequestPartition
)


@pytest.mark.roundtrip
@given(from_type(OffsetCommitRequestPartition))
def test_offset_commit_request_partition_roundtrip(
    instance: OffsetCommitRequestPartition,
) -> None:
    writer = entity_writer(OffsetCommitRequestPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_commit_request_partition(buffer)
    assert instance == result


read_offset_commit_request_topic: Final = entity_reader(OffsetCommitRequestTopic)


@pytest.mark.roundtrip
@given(from_type(OffsetCommitRequestTopic))
def test_offset_commit_request_topic_roundtrip(
    instance: OffsetCommitRequestTopic,
) -> None:
    writer = entity_writer(OffsetCommitRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_commit_request_topic(buffer)
    assert instance == result


read_offset_commit_request: Final = entity_reader(OffsetCommitRequest)


@pytest.mark.roundtrip
@given(from_type(OffsetCommitRequest))
def test_offset_commit_request_roundtrip(instance: OffsetCommitRequest) -> None:
    writer = entity_writer(OffsetCommitRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_commit_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(OffsetCommitRequest))
def test_offset_commit_request_java(
    instance: OffsetCommitRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
