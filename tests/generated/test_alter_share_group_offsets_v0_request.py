from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.alter_share_group_offsets.v0.request import (
    AlterShareGroupOffsetsRequest,
)
from kio.schema.alter_share_group_offsets.v0.request import (
    AlterShareGroupOffsetsRequestPartition,
)
from kio.schema.alter_share_group_offsets.v0.request import (
    AlterShareGroupOffsetsRequestTopic,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_alter_share_group_offsets_request_partition: Final = entity_reader(
    AlterShareGroupOffsetsRequestPartition
)


@pytest.mark.roundtrip
@given(from_type(AlterShareGroupOffsetsRequestPartition))
def test_alter_share_group_offsets_request_partition_roundtrip(
    instance: AlterShareGroupOffsetsRequestPartition,
) -> None:
    writer = entity_writer(AlterShareGroupOffsetsRequestPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_alter_share_group_offsets_request_partition(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_alter_share_group_offsets_request_topic: Final = entity_reader(
    AlterShareGroupOffsetsRequestTopic
)


@pytest.mark.roundtrip
@given(from_type(AlterShareGroupOffsetsRequestTopic))
def test_alter_share_group_offsets_request_topic_roundtrip(
    instance: AlterShareGroupOffsetsRequestTopic,
) -> None:
    writer = entity_writer(AlterShareGroupOffsetsRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_alter_share_group_offsets_request_topic(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_alter_share_group_offsets_request: Final = entity_reader(
    AlterShareGroupOffsetsRequest
)


@pytest.mark.roundtrip
@given(from_type(AlterShareGroupOffsetsRequest))
def test_alter_share_group_offsets_request_roundtrip(
    instance: AlterShareGroupOffsetsRequest,
) -> None:
    writer = entity_writer(AlterShareGroupOffsetsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_alter_share_group_offsets_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(AlterShareGroupOffsetsRequest))
def test_alter_share_group_offsets_request_java(
    instance: AlterShareGroupOffsetsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
