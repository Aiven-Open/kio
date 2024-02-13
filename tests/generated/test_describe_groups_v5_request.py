from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_groups.v5.request import DescribeGroupsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_groups_request: Final = entity_reader(DescribeGroupsRequest)


@pytest.mark.roundtrip
@given(from_type(DescribeGroupsRequest))
def test_describe_groups_request_roundtrip(instance: DescribeGroupsRequest) -> None:
    writer = entity_writer(DescribeGroupsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_groups_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeGroupsRequest))
def test_describe_groups_request_java(
    instance: DescribeGroupsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
