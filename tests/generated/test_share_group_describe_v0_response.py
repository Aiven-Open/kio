from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.share_group_describe.v0.response import Assignment
from kio.schema.share_group_describe.v0.response import DescribedGroup
from kio.schema.share_group_describe.v0.response import Member
from kio.schema.share_group_describe.v0.response import ShareGroupDescribeResponse
from kio.schema.share_group_describe.v0.response import TopicPartitions
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_topic_partitions: Final = entity_reader(TopicPartitions)


@pytest.mark.roundtrip
@given(from_type(TopicPartitions))
def test_topic_partitions_roundtrip(instance: TopicPartitions) -> None:
    writer = entity_writer(TopicPartitions)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_topic_partitions(buffer)
    assert instance == result


read_assignment: Final = entity_reader(Assignment)


@pytest.mark.roundtrip
@given(from_type(Assignment))
def test_assignment_roundtrip(instance: Assignment) -> None:
    writer = entity_writer(Assignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_assignment(buffer)
    assert instance == result


read_member: Final = entity_reader(Member)


@pytest.mark.roundtrip
@given(from_type(Member))
def test_member_roundtrip(instance: Member) -> None:
    writer = entity_writer(Member)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_member(buffer)
    assert instance == result


read_described_group: Final = entity_reader(DescribedGroup)


@pytest.mark.roundtrip
@given(from_type(DescribedGroup))
def test_described_group_roundtrip(instance: DescribedGroup) -> None:
    writer = entity_writer(DescribedGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_described_group(buffer)
    assert instance == result


read_share_group_describe_response: Final = entity_reader(ShareGroupDescribeResponse)


@pytest.mark.roundtrip
@given(from_type(ShareGroupDescribeResponse))
def test_share_group_describe_response_roundtrip(
    instance: ShareGroupDescribeResponse,
) -> None:
    writer = entity_writer(ShareGroupDescribeResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_share_group_describe_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ShareGroupDescribeResponse))
def test_share_group_describe_response_java(
    instance: ShareGroupDescribeResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
