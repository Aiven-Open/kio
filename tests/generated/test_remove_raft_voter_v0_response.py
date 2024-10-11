from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.remove_raft_voter.v0.response import RemoveRaftVoterResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_remove_raft_voter_response: Final = entity_reader(RemoveRaftVoterResponse)


@pytest.mark.roundtrip
@given(from_type(RemoveRaftVoterResponse))
def test_remove_raft_voter_response_roundtrip(
    instance: RemoveRaftVoterResponse,
) -> None:
    writer = entity_writer(RemoveRaftVoterResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_remove_raft_voter_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(RemoveRaftVoterResponse))
def test_remove_raft_voter_response_java(
    instance: RemoveRaftVoterResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
