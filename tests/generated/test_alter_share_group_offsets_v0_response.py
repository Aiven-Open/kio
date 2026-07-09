from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.alter_share_group_offsets.v0.response import (
    AlterShareGroupOffsetsResponse,
)
from kio.schema.alter_share_group_offsets.v0.response import (
    AlterShareGroupOffsetsResponsePartition,
)
from kio.schema.alter_share_group_offsets.v0.response import (
    AlterShareGroupOffsetsResponseTopic,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_alter_share_group_offsets_response_partition: Final = entity_reader(
    AlterShareGroupOffsetsResponsePartition
)


@pytest.mark.roundtrip
@given(from_type(AlterShareGroupOffsetsResponsePartition))
def test_alter_share_group_offsets_response_partition_roundtrip(
    instance: AlterShareGroupOffsetsResponsePartition,
) -> None:
    writer = entity_writer(AlterShareGroupOffsetsResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_alter_share_group_offsets_response_partition(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_alter_share_group_offsets_response_topic: Final = entity_reader(
    AlterShareGroupOffsetsResponseTopic
)


@pytest.mark.roundtrip
@given(from_type(AlterShareGroupOffsetsResponseTopic))
def test_alter_share_group_offsets_response_topic_roundtrip(
    instance: AlterShareGroupOffsetsResponseTopic,
) -> None:
    writer = entity_writer(AlterShareGroupOffsetsResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_alter_share_group_offsets_response_topic(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_alter_share_group_offsets_response: Final = entity_reader(
    AlterShareGroupOffsetsResponse
)


@pytest.mark.roundtrip
@given(from_type(AlterShareGroupOffsetsResponse))
def test_alter_share_group_offsets_response_roundtrip(
    instance: AlterShareGroupOffsetsResponse,
) -> None:
    writer = entity_writer(AlterShareGroupOffsetsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_alter_share_group_offsets_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(AlterShareGroupOffsetsResponse))
def test_alter_share_group_offsets_response_java(
    instance: AlterShareGroupOffsetsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
