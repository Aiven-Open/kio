from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.read_share_group_state.v0.response import PartitionResult
from kio.schema.read_share_group_state.v0.response import ReadShareGroupStateResponse
from kio.schema.read_share_group_state.v0.response import ReadStateResult
from kio.schema.read_share_group_state.v0.response import StateBatch
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_state_batch: Final = entity_reader(StateBatch)


@pytest.mark.roundtrip
@given(from_type(StateBatch))
def test_state_batch_roundtrip(instance: StateBatch) -> None:
    writer = entity_writer(StateBatch)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_state_batch(buffer)
    assert instance == result


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


read_read_state_result: Final = entity_reader(ReadStateResult)


@pytest.mark.roundtrip
@given(from_type(ReadStateResult))
def test_read_state_result_roundtrip(instance: ReadStateResult) -> None:
    writer = entity_writer(ReadStateResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_state_result(buffer)
    assert instance == result


read_read_share_group_state_response: Final = entity_reader(ReadShareGroupStateResponse)


@pytest.mark.roundtrip
@given(from_type(ReadShareGroupStateResponse))
def test_read_share_group_state_response_roundtrip(
    instance: ReadShareGroupStateResponse,
) -> None:
    writer = entity_writer(ReadShareGroupStateResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_share_group_state_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ReadShareGroupStateResponse))
def test_read_share_group_state_response_java(
    instance: ReadShareGroupStateResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
