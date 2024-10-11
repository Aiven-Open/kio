from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.add_raft_voter.v0.response import AddRaftVoterResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_add_raft_voter_response: Final = entity_reader(AddRaftVoterResponse)


@pytest.mark.roundtrip
@given(from_type(AddRaftVoterResponse))
def test_add_raft_voter_response_roundtrip(instance: AddRaftVoterResponse) -> None:
    writer = entity_writer(AddRaftVoterResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_raft_voter_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AddRaftVoterResponse))
def test_add_raft_voter_response_java(
    instance: AddRaftVoterResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
