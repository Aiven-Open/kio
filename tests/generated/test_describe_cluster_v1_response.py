from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_cluster.v1.response import DescribeClusterBroker
from kio.schema.describe_cluster.v1.response import DescribeClusterResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_cluster_broker: Final = entity_reader(DescribeClusterBroker)


@pytest.mark.roundtrip
@given(from_type(DescribeClusterBroker))
def test_describe_cluster_broker_roundtrip(instance: DescribeClusterBroker) -> None:
    writer = entity_writer(DescribeClusterBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_cluster_broker(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_describe_cluster_response: Final = entity_reader(DescribeClusterResponse)


@pytest.mark.roundtrip
@given(from_type(DescribeClusterResponse))
def test_describe_cluster_response_roundtrip(instance: DescribeClusterResponse) -> None:
    writer = entity_writer(DescribeClusterResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_cluster_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeClusterResponse))
def test_describe_cluster_response_java(
    instance: DescribeClusterResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
