from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.vote.v1.request import PartitionData
from kio.schema.vote.v1.request import TopicData
from kio.schema.vote.v1.request import VoteRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_partition_data: Final = entity_reader(PartitionData)


@pytest.mark.roundtrip
@given(from_type(PartitionData))
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_data(buffer)
    assert instance == result


read_topic_data: Final = entity_reader(TopicData)


@pytest.mark.roundtrip
@given(from_type(TopicData))
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_data(buffer)
    assert instance == result


read_vote_request: Final = entity_reader(VoteRequest)


@pytest.mark.roundtrip
@given(from_type(VoteRequest))
def test_vote_request_roundtrip(instance: VoteRequest) -> None:
    writer = entity_writer(VoteRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_vote_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(VoteRequest))
def test_vote_request_java(instance: VoteRequest, java_tester: JavaTester) -> None:
    java_tester.test(instance)
