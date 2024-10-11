from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.read_share_group_state.v0.request import PartitionData
from kio.schema.read_share_group_state.v0.request import ReadShareGroupStateRequest
from kio.schema.read_share_group_state.v0.request import ReadStateData
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


read_read_state_data: Final = entity_reader(ReadStateData)


@pytest.mark.roundtrip
@given(from_type(ReadStateData))
def test_read_state_data_roundtrip(instance: ReadStateData) -> None:
    writer = entity_writer(ReadStateData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_state_data(buffer)
    assert instance == result


read_read_share_group_state_request: Final = entity_reader(ReadShareGroupStateRequest)


@pytest.mark.roundtrip
@given(from_type(ReadShareGroupStateRequest))
def test_read_share_group_state_request_roundtrip(
    instance: ReadShareGroupStateRequest,
) -> None:
    writer = entity_writer(ReadShareGroupStateRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_read_share_group_state_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(ReadShareGroupStateRequest))
def test_read_share_group_state_request_java(
    instance: ReadShareGroupStateRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
