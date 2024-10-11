from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.delete_share_group_state.v0.request import DeleteShareGroupStateRequest
from kio.schema.delete_share_group_state.v0.request import DeleteStateData
from kio.schema.delete_share_group_state.v0.request import PartitionData
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


read_delete_state_data: Final = entity_reader(DeleteStateData)


@pytest.mark.roundtrip
@given(from_type(DeleteStateData))
def test_delete_state_data_roundtrip(instance: DeleteStateData) -> None:
    writer = entity_writer(DeleteStateData)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_state_data(buffer)
    assert instance == result


read_delete_share_group_state_request: Final = entity_reader(
    DeleteShareGroupStateRequest
)


@pytest.mark.roundtrip
@given(from_type(DeleteShareGroupStateRequest))
def test_delete_share_group_state_request_roundtrip(
    instance: DeleteShareGroupStateRequest,
) -> None:
    writer = entity_writer(DeleteShareGroupStateRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_share_group_state_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteShareGroupStateRequest))
def test_delete_share_group_state_request_java(
    instance: DeleteShareGroupStateRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
