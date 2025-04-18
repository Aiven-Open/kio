from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.remove_raft_voter.v0.request import RemoveRaftVoterRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_remove_raft_voter_request: Final = entity_reader(RemoveRaftVoterRequest)


@pytest.mark.roundtrip
@given(from_type(RemoveRaftVoterRequest))
def test_remove_raft_voter_request_roundtrip(instance: RemoveRaftVoterRequest) -> None:
    writer = entity_writer(RemoveRaftVoterRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_remove_raft_voter_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(RemoveRaftVoterRequest))
def test_remove_raft_voter_request_java(
    instance: RemoveRaftVoterRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
