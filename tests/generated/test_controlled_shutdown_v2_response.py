from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.controlled_shutdown.v2.response import ControlledShutdownResponse
from kio.schema.controlled_shutdown.v2.response import RemainingPartition
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_remaining_partition: Final = entity_reader(RemainingPartition)


@given(from_type(RemainingPartition))
@settings(max_examples=1)
def test_remaining_partition_roundtrip(instance: RemainingPartition) -> None:
    writer = entity_writer(RemainingPartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_remaining_partition(buffer)
    assert instance == result


read_controlled_shutdown_response: Final = entity_reader(ControlledShutdownResponse)


@given(from_type(ControlledShutdownResponse))
@settings(max_examples=1)
def test_controlled_shutdown_response_roundtrip(
    instance: ControlledShutdownResponse,
) -> None:
    writer = entity_writer(ControlledShutdownResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_controlled_shutdown_response(buffer)
    assert instance == result
