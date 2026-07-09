from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.delete_share_group_offsets.v0.request import (
    DeleteShareGroupOffsetsRequest,
)
from kio.schema.delete_share_group_offsets.v0.request import (
    DeleteShareGroupOffsetsRequestTopic,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_delete_share_group_offsets_request_topic: Final = entity_reader(
    DeleteShareGroupOffsetsRequestTopic
)


@pytest.mark.roundtrip
@given(from_type(DeleteShareGroupOffsetsRequestTopic))
def test_delete_share_group_offsets_request_topic_roundtrip(
    instance: DeleteShareGroupOffsetsRequestTopic,
) -> None:
    writer = entity_writer(DeleteShareGroupOffsetsRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_delete_share_group_offsets_request_topic(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_delete_share_group_offsets_request: Final = entity_reader(
    DeleteShareGroupOffsetsRequest
)


@pytest.mark.roundtrip
@given(from_type(DeleteShareGroupOffsetsRequest))
def test_delete_share_group_offsets_request_roundtrip(
    instance: DeleteShareGroupOffsetsRequest,
) -> None:
    writer = entity_writer(DeleteShareGroupOffsetsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_delete_share_group_offsets_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteShareGroupOffsetsRequest))
def test_delete_share_group_offsets_request_java(
    instance: DeleteShareGroupOffsetsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
