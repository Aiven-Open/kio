from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leader_and_isr.v2.response import LeaderAndIsrPartitionError
from kio.schema.leader_and_isr.v2.response import LeaderAndIsrResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_leader_and_isr_partition_error: Final = entity_reader(LeaderAndIsrPartitionError)


@pytest.mark.roundtrip
@given(from_type(LeaderAndIsrPartitionError))
@settings(max_examples=1)
def test_leader_and_isr_partition_error_roundtrip(
    instance: LeaderAndIsrPartitionError,
) -> None:
    writer = entity_writer(LeaderAndIsrPartitionError)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_and_isr_partition_error(buffer)
    assert instance == result


read_leader_and_isr_response: Final = entity_reader(LeaderAndIsrResponse)


@pytest.mark.roundtrip
@given(from_type(LeaderAndIsrResponse))
@settings(max_examples=1)
def test_leader_and_isr_response_roundtrip(instance: LeaderAndIsrResponse) -> None:
    writer = entity_writer(LeaderAndIsrResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_and_isr_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(LeaderAndIsrResponse))
def test_leader_and_isr_response_java(
    instance: LeaderAndIsrResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
