from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.write_share_group_state.v0.response import PartitionResult
from kio.schema.write_share_group_state.v0.response import WriteShareGroupStateResponse
from kio.schema.write_share_group_state.v0.response import WriteStateResult
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


read_write_state_result: Final = entity_reader(WriteStateResult)


@pytest.mark.roundtrip
@given(from_type(WriteStateResult))
def test_write_state_result_roundtrip(instance: WriteStateResult) -> None:
    writer = entity_writer(WriteStateResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_write_state_result(buffer)
    assert instance == result


read_write_share_group_state_response: Final = entity_reader(
    WriteShareGroupStateResponse
)


@pytest.mark.roundtrip
@given(from_type(WriteShareGroupStateResponse))
def test_write_share_group_state_response_roundtrip(
    instance: WriteShareGroupStateResponse,
) -> None:
    writer = entity_writer(WriteShareGroupStateResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_write_share_group_state_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(WriteShareGroupStateResponse))
def test_write_share_group_state_response_java(
    instance: WriteShareGroupStateResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
