from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.describe_share_group_offsets.v0.response import (
    DescribeShareGroupOffsetsResponse,
)
from kio.schema.describe_share_group_offsets.v0.response import (
    DescribeShareGroupOffsetsResponseGroup,
)
from kio.schema.describe_share_group_offsets.v0.response import (
    DescribeShareGroupOffsetsResponsePartition,
)
from kio.schema.describe_share_group_offsets.v0.response import (
    DescribeShareGroupOffsetsResponseTopic,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_describe_share_group_offsets_response_partition: Final = entity_reader(
    DescribeShareGroupOffsetsResponsePartition
)


@pytest.mark.roundtrip
@given(from_type(DescribeShareGroupOffsetsResponsePartition))
def test_describe_share_group_offsets_response_partition_roundtrip(
    instance: DescribeShareGroupOffsetsResponsePartition,
) -> None:
    writer = entity_writer(DescribeShareGroupOffsetsResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_share_group_offsets_response_partition(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_describe_share_group_offsets_response_topic: Final = entity_reader(
    DescribeShareGroupOffsetsResponseTopic
)


@pytest.mark.roundtrip
@given(from_type(DescribeShareGroupOffsetsResponseTopic))
def test_describe_share_group_offsets_response_topic_roundtrip(
    instance: DescribeShareGroupOffsetsResponseTopic,
) -> None:
    writer = entity_writer(DescribeShareGroupOffsetsResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_share_group_offsets_response_topic(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_describe_share_group_offsets_response_group: Final = entity_reader(
    DescribeShareGroupOffsetsResponseGroup
)


@pytest.mark.roundtrip
@given(from_type(DescribeShareGroupOffsetsResponseGroup))
def test_describe_share_group_offsets_response_group_roundtrip(
    instance: DescribeShareGroupOffsetsResponseGroup,
) -> None:
    writer = entity_writer(DescribeShareGroupOffsetsResponseGroup)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_share_group_offsets_response_group(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_describe_share_group_offsets_response: Final = entity_reader(
    DescribeShareGroupOffsetsResponse
)


@pytest.mark.roundtrip
@given(from_type(DescribeShareGroupOffsetsResponse))
def test_describe_share_group_offsets_response_roundtrip(
    instance: DescribeShareGroupOffsetsResponse,
) -> None:
    writer = entity_writer(DescribeShareGroupOffsetsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_describe_share_group_offsets_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(DescribeShareGroupOffsetsResponse))
def test_describe_share_group_offsets_response_java(
    instance: DescribeShareGroupOffsetsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
