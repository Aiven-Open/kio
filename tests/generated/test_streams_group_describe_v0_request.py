from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.streams_group_describe.v0.request import StreamsGroupDescribeRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_streams_group_describe_request: Final = entity_reader(StreamsGroupDescribeRequest)


@pytest.mark.roundtrip
@given(from_type(StreamsGroupDescribeRequest))
def test_streams_group_describe_request_roundtrip(
    instance: StreamsGroupDescribeRequest,
) -> None:
    writer = entity_writer(StreamsGroupDescribeRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_streams_group_describe_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(StreamsGroupDescribeRequest))
def test_streams_group_describe_request_java(
    instance: StreamsGroupDescribeRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
