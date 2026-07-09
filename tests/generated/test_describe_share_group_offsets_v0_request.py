from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_share_group_offsets.v0.request import (
    DescribeShareGroupOffsetsRequest,
)
from kio.schema.describe_share_group_offsets.v0.request import (
    DescribeShareGroupOffsetsRequestGroup,
)
from kio.schema.describe_share_group_offsets.v0.request import (
    DescribeShareGroupOffsetsRequestTopic,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_share_group_offsets_request_topic: Final = entity_reader(
    DescribeShareGroupOffsetsRequestTopic
)


@pytest.mark.roundtrip
@given(from_type(DescribeShareGroupOffsetsRequestTopic))
def test_describe_share_group_offsets_request_topic_roundtrip(
    instance: DescribeShareGroupOffsetsRequestTopic,
) -> None:
    writer = entity_writer(DescribeShareGroupOffsetsRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_share_group_offsets_request_topic(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_describe_share_group_offsets_request_group: Final = entity_reader(
    DescribeShareGroupOffsetsRequestGroup
)


@pytest.mark.roundtrip
@given(from_type(DescribeShareGroupOffsetsRequestGroup))
def test_describe_share_group_offsets_request_group_roundtrip(
    instance: DescribeShareGroupOffsetsRequestGroup,
) -> None:
    writer = entity_writer(DescribeShareGroupOffsetsRequestGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_share_group_offsets_request_group(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_describe_share_group_offsets_request: Final = entity_reader(
    DescribeShareGroupOffsetsRequest
)


@pytest.mark.roundtrip
@given(from_type(DescribeShareGroupOffsetsRequest))
def test_describe_share_group_offsets_request_roundtrip(
    instance: DescribeShareGroupOffsetsRequest,
) -> None:
    writer = entity_writer(DescribeShareGroupOffsetsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_share_group_offsets_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeShareGroupOffsetsRequest))
def test_describe_share_group_offsets_request_java(
    instance: DescribeShareGroupOffsetsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
