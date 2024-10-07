from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.update_raft_voter.v0.response import CurrentLeader
from kio.schema.update_raft_voter.v0.response import UpdateRaftVoterResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_current_leader: Final = entity_reader(CurrentLeader)


@pytest.mark.roundtrip
@given(from_type(CurrentLeader))
def test_current_leader_roundtrip(instance: CurrentLeader) -> None:
    writer = entity_writer(CurrentLeader)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_current_leader(buffer)
    assert instance == result


read_update_raft_voter_response: Final = entity_reader(UpdateRaftVoterResponse)


@pytest.mark.roundtrip
@given(from_type(UpdateRaftVoterResponse))
def test_update_raft_voter_response_roundtrip(
    instance: UpdateRaftVoterResponse,
) -> None:
    writer = entity_writer(UpdateRaftVoterResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_raft_voter_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateRaftVoterResponse))
def test_update_raft_voter_response_java(
    instance: UpdateRaftVoterResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
