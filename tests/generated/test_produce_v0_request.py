from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.produce.v0.request import PartitionProduceData
from kio.schema.produce.v0.request import ProduceRequest
from kio.schema.produce.v0.request import TopicProduceData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_partition_produce_data: Final = entity_reader(PartitionProduceData)


@pytest.mark.roundtrip
@given(from_type(PartitionProduceData))
@settings(max_examples=1)
def test_partition_produce_data_roundtrip(instance: PartitionProduceData) -> None:
    writer = entity_writer(PartitionProduceData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_produce_data(buffer)
    assert instance == result


read_topic_produce_data: Final = entity_reader(TopicProduceData)


@pytest.mark.roundtrip
@given(from_type(TopicProduceData))
@settings(max_examples=1)
def test_topic_produce_data_roundtrip(instance: TopicProduceData) -> None:
    writer = entity_writer(TopicProduceData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_produce_data(buffer)
    assert instance == result


read_produce_request: Final = entity_reader(ProduceRequest)


@pytest.mark.roundtrip
@given(from_type(ProduceRequest))
@settings(max_examples=1)
def test_produce_request_roundtrip(instance: ProduceRequest) -> None:
    writer = entity_writer(ProduceRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_produce_request(buffer)
    assert instance == result
