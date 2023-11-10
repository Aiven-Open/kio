from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.describe_cluster.v0.response import DescribeClusterBroker
from kio.schema.describe_cluster.v0.response import DescribeClusterResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_cluster_broker: Final = entity_reader(DescribeClusterBroker)


@given(from_type(DescribeClusterBroker))
@settings(max_examples=1)
def test_describe_cluster_broker_roundtrip(instance: DescribeClusterBroker) -> None:
    writer = entity_writer(DescribeClusterBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_cluster_broker(buffer)
    assert instance == result


read_describe_cluster_response: Final = entity_reader(DescribeClusterResponse)


@given(from_type(DescribeClusterResponse))
@settings(max_examples=1)
def test_describe_cluster_response_roundtrip(instance: DescribeClusterResponse) -> None:
    writer = entity_writer(DescribeClusterResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_describe_cluster_response(buffer)
    assert instance == result


@given(instance=from_type(DescribeClusterResponse))
def test_describe_cluster_response_java(
    instance: DescribeClusterResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
