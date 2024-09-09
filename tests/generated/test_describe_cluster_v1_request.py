from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_cluster.v1.request import DescribeClusterRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_cluster_request: Final = entity_reader(DescribeClusterRequest)


@pytest.mark.roundtrip
@given(from_type(DescribeClusterRequest))
def test_describe_cluster_request_roundtrip(instance: DescribeClusterRequest) -> None:
    writer = entity_writer(DescribeClusterRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_cluster_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeClusterRequest))
def test_describe_cluster_request_java(
    instance: DescribeClusterRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
