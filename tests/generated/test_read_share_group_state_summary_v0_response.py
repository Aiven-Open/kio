from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.read_share_group_state_summary.v0.response import PartitionResult
from kio.schema.read_share_group_state_summary.v0.response import (
    ReadShareGroupStateSummaryResponse,
)
from kio.schema.read_share_group_state_summary.v0.response import ReadStateSummaryResult
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


read_read_state_summary_result: Final = entity_reader(ReadStateSummaryResult)


@pytest.mark.roundtrip
@given(from_type(ReadStateSummaryResult))
def test_read_state_summary_result_roundtrip(instance: ReadStateSummaryResult) -> None:
    writer = entity_writer(ReadStateSummaryResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_state_summary_result(buffer)
    assert instance == result


read_read_share_group_state_summary_response: Final = entity_reader(
    ReadShareGroupStateSummaryResponse
)


@pytest.mark.roundtrip
@given(from_type(ReadShareGroupStateSummaryResponse))
def test_read_share_group_state_summary_response_roundtrip(
    instance: ReadShareGroupStateSummaryResponse,
) -> None:
    writer = entity_writer(ReadShareGroupStateSummaryResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_share_group_state_summary_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ReadShareGroupStateSummaryResponse))
def test_read_share_group_state_summary_response_java(
    instance: ReadShareGroupStateSummaryResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
