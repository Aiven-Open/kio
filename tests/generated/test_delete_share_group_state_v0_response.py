from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.delete_share_group_state.v0.response import (
    DeleteShareGroupStateResponse,
)
from kio.schema.delete_share_group_state.v0.response import DeleteStateResult
from kio.schema.delete_share_group_state.v0.response import PartitionResult
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_partition_result: Final = entity_reader(PartitionResult)


@pytest.mark.roundtrip
@given(from_type(PartitionResult))
def test_partition_result_roundtrip(instance: PartitionResult) -> None:
    writer = entity_writer(PartitionResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_result(buffer)
    assert instance == result


read_delete_state_result: Final = entity_reader(DeleteStateResult)


@pytest.mark.roundtrip
@given(from_type(DeleteStateResult))
def test_delete_state_result_roundtrip(instance: DeleteStateResult) -> None:
    writer = entity_writer(DeleteStateResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_state_result(buffer)
    assert instance == result


read_delete_share_group_state_response: Final = entity_reader(
    DeleteShareGroupStateResponse
)


@pytest.mark.roundtrip
@given(from_type(DeleteShareGroupStateResponse))
def test_delete_share_group_state_response_roundtrip(
    instance: DeleteShareGroupStateResponse,
) -> None:
    writer = entity_writer(DeleteShareGroupStateResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_share_group_state_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteShareGroupStateResponse))
def test_delete_share_group_state_response_java(
    instance: DeleteShareGroupStateResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
