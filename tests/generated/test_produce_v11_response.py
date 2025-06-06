from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.produce.v11.response import BatchIndexAndErrorMessage
from kio.schema.produce.v11.response import LeaderIdAndEpoch
from kio.schema.produce.v11.response import NodeEndpoint
from kio.schema.produce.v11.response import PartitionProduceResponse
from kio.schema.produce.v11.response import ProduceResponse
from kio.schema.produce.v11.response import TopicProduceResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_batch_index_and_error_message: Final = entity_reader(BatchIndexAndErrorMessage)


@pytest.mark.roundtrip
@given(from_type(BatchIndexAndErrorMessage))
def test_batch_index_and_error_message_roundtrip(
    instance: BatchIndexAndErrorMessage,
) -> None:
    writer = entity_writer(BatchIndexAndErrorMessage)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_batch_index_and_error_message(buffer)
    assert instance == result


read_leader_id_and_epoch: Final = entity_reader(LeaderIdAndEpoch)


@pytest.mark.roundtrip
@given(from_type(LeaderIdAndEpoch))
def test_leader_id_and_epoch_roundtrip(instance: LeaderIdAndEpoch) -> None:
    writer = entity_writer(LeaderIdAndEpoch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_id_and_epoch(buffer)
    assert instance == result


read_partition_produce_response: Final = entity_reader(PartitionProduceResponse)


@pytest.mark.roundtrip
@given(from_type(PartitionProduceResponse))
def test_partition_produce_response_roundtrip(
    instance: PartitionProduceResponse,
) -> None:
    writer = entity_writer(PartitionProduceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_produce_response(buffer)
    assert instance == result


read_topic_produce_response: Final = entity_reader(TopicProduceResponse)


@pytest.mark.roundtrip
@given(from_type(TopicProduceResponse))
def test_topic_produce_response_roundtrip(instance: TopicProduceResponse) -> None:
    writer = entity_writer(TopicProduceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_produce_response(buffer)
    assert instance == result


read_node_endpoint: Final = entity_reader(NodeEndpoint)


@pytest.mark.roundtrip
@given(from_type(NodeEndpoint))
def test_node_endpoint_roundtrip(instance: NodeEndpoint) -> None:
    writer = entity_writer(NodeEndpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_node_endpoint(buffer)
    assert instance == result


read_produce_response: Final = entity_reader(ProduceResponse)


@pytest.mark.roundtrip
@given(from_type(ProduceResponse))
def test_produce_response_roundtrip(instance: ProduceResponse) -> None:
    writer = entity_writer(ProduceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_produce_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ProduceResponse))
def test_produce_response_java(
    instance: ProduceResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
