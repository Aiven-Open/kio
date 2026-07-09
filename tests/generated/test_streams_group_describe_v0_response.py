from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.streams_group_describe.v0.response import Assignment
from kio.schema.streams_group_describe.v0.response import DescribedGroup
from kio.schema.streams_group_describe.v0.response import Endpoint
from kio.schema.streams_group_describe.v0.response import KeyValue
from kio.schema.streams_group_describe.v0.response import Member
from kio.schema.streams_group_describe.v0.response import StreamsGroupDescribeResponse
from kio.schema.streams_group_describe.v0.response import Subtopology
from kio.schema.streams_group_describe.v0.response import TaskIds
from kio.schema.streams_group_describe.v0.response import TaskOffset
from kio.schema.streams_group_describe.v0.response import TopicInfo
from kio.schema.streams_group_describe.v0.response import Topology
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


read_assignment: Final = entity_reader(Assignment)


@pytest.mark.roundtrip
@given(from_type(Assignment))
def test_assignment_roundtrip(instance: Assignment) -> None:
    writer = entity_writer(Assignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_assignment(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_member: Final = entity_reader(Member)


@pytest.mark.roundtrip
@given(from_type(Member))
def test_member_roundtrip(instance: Member) -> None:
    writer = entity_writer(Member)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_member(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_described_group: Final = entity_reader(DescribedGroup)


@pytest.mark.roundtrip
@given(from_type(DescribedGroup))
def test_described_group_roundtrip(instance: DescribedGroup) -> None:
    writer = entity_writer(DescribedGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_described_group(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_streams_group_describe_response: Final = entity_reader(
    StreamsGroupDescribeResponse
)


@pytest.mark.roundtrip
@given(from_type(StreamsGroupDescribeResponse))
def test_streams_group_describe_response_roundtrip(
    instance: StreamsGroupDescribeResponse,
) -> None:
    writer = entity_writer(StreamsGroupDescribeResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_streams_group_describe_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(StreamsGroupDescribeResponse))
def test_streams_group_describe_response_java(
    instance: StreamsGroupDescribeResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
