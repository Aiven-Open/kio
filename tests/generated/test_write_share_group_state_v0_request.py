from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.write_share_group_state.v0.request import PartitionData
from kio.schema.write_share_group_state.v0.request import StateBatch
from kio.schema.write_share_group_state.v0.request import WriteShareGroupStateRequest
from kio.schema.write_share_group_state.v0.request import WriteStateData
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


read_write_state_data: Final = entity_reader(WriteStateData)


@pytest.mark.roundtrip
@given(from_type(WriteStateData))
def test_write_state_data_roundtrip(instance: WriteStateData) -> None:
    writer = entity_writer(WriteStateData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_write_state_data(buffer)
    assert instance == result


read_write_share_group_state_request: Final = entity_reader(WriteShareGroupStateRequest)


@pytest.mark.roundtrip
@given(from_type(WriteShareGroupStateRequest))
def test_write_share_group_state_request_roundtrip(
    instance: WriteShareGroupStateRequest,
) -> None:
    writer = entity_writer(WriteShareGroupStateRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_write_share_group_state_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(WriteShareGroupStateRequest))
def test_write_share_group_state_request_java(
    instance: WriteShareGroupStateRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
