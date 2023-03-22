from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.elect_leaders.v0.request import ElectLeadersRequest
from kio.schema.elect_leaders.v0.request import TopicPartitions
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_topic_partitions: Final = entity_reader(TopicPartitions)


@given(from_type(TopicPartitions))
@settings(max_examples=1)
def test_topic_partitions_roundtrip(instance: TopicPartitions) -> None:
    writer = entity_writer(TopicPartitions)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_partitions(buffer)
    assert instance == result


read_elect_leaders_request: Final = entity_reader(ElectLeadersRequest)


@given(from_type(ElectLeadersRequest))
@settings(max_examples=1)
def test_elect_leaders_request_roundtrip(instance: ElectLeadersRequest) -> None:
    writer = entity_writer(ElectLeadersRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_elect_leaders_request(buffer)
    assert instance == result
