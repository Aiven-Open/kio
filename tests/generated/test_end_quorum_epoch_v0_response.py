from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.end_quorum_epoch.v0.response import EndQuorumEpochResponse
from kio.schema.end_quorum_epoch.v0.response import PartitionData
from kio.schema.end_quorum_epoch.v0.response import TopicData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_partition_data: Final = entity_reader(PartitionData)


@given(from_type(PartitionData))
@settings(max_examples=1)
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_data(buffer)
    assert instance == result


read_topic_data: Final = entity_reader(TopicData)


@given(from_type(TopicData))
@settings(max_examples=1)
def test_topic_data_roundtrip(instance: TopicData) -> None:
    writer = entity_writer(TopicData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_data(buffer)
    assert instance == result


read_end_quorum_epoch_response: Final = entity_reader(EndQuorumEpochResponse)


@given(from_type(EndQuorumEpochResponse))
@settings(max_examples=1)
def test_end_quorum_epoch_response_roundtrip(instance: EndQuorumEpochResponse) -> None:
    writer = entity_writer(EndQuorumEpochResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_end_quorum_epoch_response(buffer)
    assert instance == result
