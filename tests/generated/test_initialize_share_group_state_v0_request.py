from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.initialize_share_group_state.v0.request import (
    InitializeShareGroupStateRequest,
)
from kio.schema.initialize_share_group_state.v0.request import InitializeStateData
from kio.schema.initialize_share_group_state.v0.request import PartitionData
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


read_initialize_state_data: Final = entity_reader(InitializeStateData)


@pytest.mark.roundtrip
@given(from_type(InitializeStateData))
def test_initialize_state_data_roundtrip(instance: InitializeStateData) -> None:
    writer = entity_writer(InitializeStateData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_initialize_state_data(buffer)
    assert instance == result


read_initialize_share_group_state_request: Final = entity_reader(
    InitializeShareGroupStateRequest
)


@pytest.mark.roundtrip
@given(from_type(InitializeShareGroupStateRequest))
def test_initialize_share_group_state_request_roundtrip(
    instance: InitializeShareGroupStateRequest,
) -> None:
    writer = entity_writer(InitializeShareGroupStateRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_initialize_share_group_state_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(InitializeShareGroupStateRequest))
def test_initialize_share_group_state_request_java(
    instance: InitializeShareGroupStateRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
