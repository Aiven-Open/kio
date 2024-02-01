from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.offset_commit.v5.response import OffsetCommitResponse
from kio.schema.offset_commit.v5.response import OffsetCommitResponsePartition
from kio.schema.offset_commit.v5.response import OffsetCommitResponseTopic
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_offset_commit_response_partition: Final = entity_reader(
    OffsetCommitResponsePartition
)


@pytest.mark.roundtrip
@given(from_type(OffsetCommitResponsePartition))
def test_offset_commit_response_partition_roundtrip(
    instance: OffsetCommitResponsePartition,
) -> None:
    writer = entity_writer(OffsetCommitResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_commit_response_partition(buffer)
    assert instance == result


read_offset_commit_response_topic: Final = entity_reader(OffsetCommitResponseTopic)


@pytest.mark.roundtrip
@given(from_type(OffsetCommitResponseTopic))
def test_offset_commit_response_topic_roundtrip(
    instance: OffsetCommitResponseTopic,
) -> None:
    writer = entity_writer(OffsetCommitResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_commit_response_topic(buffer)
    assert instance == result


read_offset_commit_response: Final = entity_reader(OffsetCommitResponse)


@pytest.mark.roundtrip
@given(from_type(OffsetCommitResponse))
def test_offset_commit_response_roundtrip(instance: OffsetCommitResponse) -> None:
    writer = entity_writer(OffsetCommitResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_offset_commit_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(OffsetCommitResponse))
def test_offset_commit_response_java(
    instance: OffsetCommitResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
