from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.delete_share_group_offsets.v0.response import (
    DeleteShareGroupOffsetsResponse,
)
from kio.schema.delete_share_group_offsets.v0.response import (
    DeleteShareGroupOffsetsResponseTopic,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_delete_share_group_offsets_response_topic: Final = entity_reader(
    DeleteShareGroupOffsetsResponseTopic
)


@pytest.mark.roundtrip
@given(from_type(DeleteShareGroupOffsetsResponseTopic))
def test_delete_share_group_offsets_response_topic_roundtrip(
    instance: DeleteShareGroupOffsetsResponseTopic,
) -> None:
    writer = entity_writer(DeleteShareGroupOffsetsResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_delete_share_group_offsets_response_topic(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_delete_share_group_offsets_response: Final = entity_reader(
    DeleteShareGroupOffsetsResponse
)


@pytest.mark.roundtrip
@given(from_type(DeleteShareGroupOffsetsResponse))
def test_delete_share_group_offsets_response_roundtrip(
    instance: DeleteShareGroupOffsetsResponse,
) -> None:
    writer = entity_writer(DeleteShareGroupOffsetsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_delete_share_group_offsets_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteShareGroupOffsetsResponse))
def test_delete_share_group_offsets_response_java(
    instance: DeleteShareGroupOffsetsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
