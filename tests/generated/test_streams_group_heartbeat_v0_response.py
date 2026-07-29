from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.streams_group_heartbeat.v0.response import Endpoint
from kio.schema.streams_group_heartbeat.v0.response import EndpointToPartitions
from kio.schema.streams_group_heartbeat.v0.response import Status
from kio.schema.streams_group_heartbeat.v0.response import StreamsGroupHeartbeatResponse
from kio.schema.streams_group_heartbeat.v0.response import TaskIds
from kio.schema.streams_group_heartbeat.v0.response import TopicPartition
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_status: Final = entity_reader(Status)


@pytest.mark.roundtrip
@given(from_type(Status))
def test_status_roundtrip(instance: Status) -> None:
    writer = entity_writer(Status)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_status(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_task_ids: Final = entity_reader(TaskIds)


@pytest.mark.roundtrip
@given(from_type(TaskIds))
def test_task_ids_roundtrip(instance: TaskIds) -> None:
    writer = entity_writer(TaskIds)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_task_ids(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_endpoint: Final = entity_reader(Endpoint)


@pytest.mark.roundtrip
@given(from_type(Endpoint))
def test_endpoint_roundtrip(instance: Endpoint) -> None:
    writer = entity_writer(Endpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_endpoint(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_topic_partition: Final = entity_reader(TopicPartition)


@pytest.mark.roundtrip
@given(from_type(TopicPartition))
def test_topic_partition_roundtrip(instance: TopicPartition) -> None:
    writer = entity_writer(TopicPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_topic_partition(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_endpoint_to_partitions: Final = entity_reader(EndpointToPartitions)


@pytest.mark.roundtrip
@given(from_type(EndpointToPartitions))
def test_endpoint_to_partitions_roundtrip(instance: EndpointToPartitions) -> None:
    writer = entity_writer(EndpointToPartitions)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_endpoint_to_partitions(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_streams_group_heartbeat_response: Final = entity_reader(
    StreamsGroupHeartbeatResponse
)


@pytest.mark.roundtrip
@given(from_type(StreamsGroupHeartbeatResponse))
def test_streams_group_heartbeat_response_roundtrip(
    instance: StreamsGroupHeartbeatResponse,
) -> None:
    writer = entity_writer(StreamsGroupHeartbeatResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_streams_group_heartbeat_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(StreamsGroupHeartbeatResponse))
def test_streams_group_heartbeat_response_java(
    instance: StreamsGroupHeartbeatResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
