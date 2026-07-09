from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.streams_group_heartbeat.v0.request import CopartitionGroup
from kio.schema.streams_group_heartbeat.v0.request import Endpoint
from kio.schema.streams_group_heartbeat.v0.request import KeyValue
from kio.schema.streams_group_heartbeat.v0.request import StreamsGroupHeartbeatRequest
from kio.schema.streams_group_heartbeat.v0.request import Subtopology
from kio.schema.streams_group_heartbeat.v0.request import TaskIds
from kio.schema.streams_group_heartbeat.v0.request import TaskOffset
from kio.schema.streams_group_heartbeat.v0.request import TopicInfo
from kio.schema.streams_group_heartbeat.v0.request import Topology
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_key_value: Final = entity_reader(KeyValue)


@pytest.mark.roundtrip
@given(from_type(KeyValue))
def test_key_value_roundtrip(instance: KeyValue) -> None:
    writer = entity_writer(KeyValue)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_key_value(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_topic_info: Final = entity_reader(TopicInfo)


@pytest.mark.roundtrip
@given(from_type(TopicInfo))
def test_topic_info_roundtrip(instance: TopicInfo) -> None:
    writer = entity_writer(TopicInfo)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_topic_info(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_copartition_group: Final = entity_reader(CopartitionGroup)


@pytest.mark.roundtrip
@given(from_type(CopartitionGroup))
def test_copartition_group_roundtrip(instance: CopartitionGroup) -> None:
    writer = entity_writer(CopartitionGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_copartition_group(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_subtopology: Final = entity_reader(Subtopology)


@pytest.mark.roundtrip
@given(from_type(Subtopology))
def test_subtopology_roundtrip(instance: Subtopology) -> None:
    writer = entity_writer(Subtopology)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_subtopology(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_topology: Final = entity_reader(Topology)


@pytest.mark.roundtrip
@given(from_type(Topology))
def test_topology_roundtrip(instance: Topology) -> None:
    writer = entity_writer(Topology)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_topology(
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


read_task_offset: Final = entity_reader(TaskOffset)


@pytest.mark.roundtrip
@given(from_type(TaskOffset))
def test_task_offset_roundtrip(instance: TaskOffset) -> None:
    writer = entity_writer(TaskOffset)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_task_offset(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_streams_group_heartbeat_request: Final = entity_reader(
    StreamsGroupHeartbeatRequest
)


@pytest.mark.roundtrip
@given(from_type(StreamsGroupHeartbeatRequest))
def test_streams_group_heartbeat_request_roundtrip(
    instance: StreamsGroupHeartbeatRequest,
) -> None:
    writer = entity_writer(StreamsGroupHeartbeatRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_streams_group_heartbeat_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(StreamsGroupHeartbeatRequest))
def test_streams_group_heartbeat_request_java(
    instance: StreamsGroupHeartbeatRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
