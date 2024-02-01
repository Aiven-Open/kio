from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leader_and_isr.v4.request import LeaderAndIsrLiveLeader
from kio.schema.leader_and_isr.v4.request import LeaderAndIsrPartitionState
from kio.schema.leader_and_isr.v4.request import LeaderAndIsrRequest
from kio.schema.leader_and_isr.v4.request import LeaderAndIsrTopicState
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_leader_and_isr_partition_state: Final = entity_reader(LeaderAndIsrPartitionState)


@pytest.mark.roundtrip
@given(from_type(LeaderAndIsrPartitionState))
@settings(max_examples=1)
def test_leader_and_isr_partition_state_roundtrip(
    instance: LeaderAndIsrPartitionState,
) -> None:
    writer = entity_writer(LeaderAndIsrPartitionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_and_isr_partition_state(buffer)
    assert instance == result


read_leader_and_isr_topic_state: Final = entity_reader(LeaderAndIsrTopicState)


@pytest.mark.roundtrip
@given(from_type(LeaderAndIsrTopicState))
@settings(max_examples=1)
def test_leader_and_isr_topic_state_roundtrip(instance: LeaderAndIsrTopicState) -> None:
    writer = entity_writer(LeaderAndIsrTopicState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_and_isr_topic_state(buffer)
    assert instance == result


read_leader_and_isr_live_leader: Final = entity_reader(LeaderAndIsrLiveLeader)


@pytest.mark.roundtrip
@given(from_type(LeaderAndIsrLiveLeader))
@settings(max_examples=1)
def test_leader_and_isr_live_leader_roundtrip(instance: LeaderAndIsrLiveLeader) -> None:
    writer = entity_writer(LeaderAndIsrLiveLeader)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_and_isr_live_leader(buffer)
    assert instance == result


read_leader_and_isr_request: Final = entity_reader(LeaderAndIsrRequest)


@pytest.mark.roundtrip
@given(from_type(LeaderAndIsrRequest))
@settings(max_examples=1)
def test_leader_and_isr_request_roundtrip(instance: LeaderAndIsrRequest) -> None:
    writer = entity_writer(LeaderAndIsrRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_and_isr_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(LeaderAndIsrRequest))
def test_leader_and_isr_request_java(
    instance: LeaderAndIsrRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
