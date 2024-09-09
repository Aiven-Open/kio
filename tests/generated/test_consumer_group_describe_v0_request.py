from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.consumer_group_describe.v0.request import ConsumerGroupDescribeRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_consumer_group_describe_request: Final = entity_reader(
    ConsumerGroupDescribeRequest
)


@pytest.mark.roundtrip
@given(from_type(ConsumerGroupDescribeRequest))
def test_consumer_group_describe_request_roundtrip(
    instance: ConsumerGroupDescribeRequest,
) -> None:
    writer = entity_writer(ConsumerGroupDescribeRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_consumer_group_describe_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ConsumerGroupDescribeRequest))
def test_consumer_group_describe_request_java(
    instance: ConsumerGroupDescribeRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
