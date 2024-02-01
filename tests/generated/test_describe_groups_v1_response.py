from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_groups.v1.response import DescribedGroup
from kio.schema.describe_groups.v1.response import DescribedGroupMember
from kio.schema.describe_groups.v1.response import DescribeGroupsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_described_group_member: Final = entity_reader(DescribedGroupMember)


@pytest.mark.roundtrip
@given(from_type(DescribedGroupMember))
def test_described_group_member_roundtrip(instance: DescribedGroupMember) -> None:
    writer = entity_writer(DescribedGroupMember)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_described_group_member(buffer)
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


read_describe_groups_response: Final = entity_reader(DescribeGroupsResponse)


@pytest.mark.roundtrip
@given(from_type(DescribeGroupsResponse))
def test_describe_groups_response_roundtrip(instance: DescribeGroupsResponse) -> None:
    writer = entity_writer(DescribeGroupsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_groups_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeGroupsResponse))
def test_describe_groups_response_java(
    instance: DescribeGroupsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
