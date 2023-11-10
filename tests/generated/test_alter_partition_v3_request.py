from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_partition.v3.request import AlterPartitionRequest
from kio.schema.alter_partition.v3.request import BrokerState
from kio.schema.alter_partition.v3.request import PartitionData
from kio.schema.alter_partition.v3.request import TopicData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_broker_state: Final = entity_reader(BrokerState)


@given(from_type(BrokerState))
@settings(max_examples=1)
def test_broker_state_roundtrip(instance: BrokerState) -> None:
    writer = entity_writer(BrokerState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_broker_state(buffer)
    assert instance == result


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


read_alter_partition_request: Final = entity_reader(AlterPartitionRequest)


@given(from_type(AlterPartitionRequest))
@settings(max_examples=1)
def test_alter_partition_request_roundtrip(instance: AlterPartitionRequest) -> None:
    writer = entity_writer(AlterPartitionRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_partition_request(buffer)
    assert instance == result


@given(instance=from_type(AlterPartitionRequest))
def test_alter_partition_request_java(
    instance: AlterPartitionRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
