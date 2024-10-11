from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.read_share_group_state_summary.v0.request import PartitionData
from kio.schema.read_share_group_state_summary.v0.request import (
    ReadShareGroupStateSummaryRequest,
)
from kio.schema.read_share_group_state_summary.v0.request import ReadStateSummaryData
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_partition_data: Final = entity_reader(PartitionData)


@pytest.mark.roundtrip
@given(from_type(PartitionData))
def test_partition_data_roundtrip(instance: PartitionData) -> None:
    writer = entity_writer(PartitionData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_partition_data(buffer)
    assert instance == result


read_read_state_summary_data: Final = entity_reader(ReadStateSummaryData)


@pytest.mark.roundtrip
@given(from_type(ReadStateSummaryData))
def test_read_state_summary_data_roundtrip(instance: ReadStateSummaryData) -> None:
    writer = entity_writer(ReadStateSummaryData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_state_summary_data(buffer)
    assert instance == result


read_read_share_group_state_summary_request: Final = entity_reader(
    ReadShareGroupStateSummaryRequest
)


@pytest.mark.roundtrip
@given(from_type(ReadShareGroupStateSummaryRequest))
def test_read_share_group_state_summary_request_roundtrip(
    instance: ReadShareGroupStateSummaryRequest,
) -> None:
    writer = entity_writer(ReadShareGroupStateSummaryRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_share_group_state_summary_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ReadShareGroupStateSummaryRequest))
def test_read_share_group_state_summary_request_java(
    instance: ReadShareGroupStateSummaryRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
