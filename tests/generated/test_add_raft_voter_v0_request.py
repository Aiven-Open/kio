from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.add_raft_voter.v0.request import AddRaftVoterRequest
from kio.schema.add_raft_voter.v0.request import Listener
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_listener: Final = entity_reader(Listener)


@pytest.mark.roundtrip
@given(from_type(Listener))
def test_listener_roundtrip(instance: Listener) -> None:
    writer = entity_writer(Listener)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_listener(buffer)
    assert instance == result


read_add_raft_voter_request: Final = entity_reader(AddRaftVoterRequest)


@pytest.mark.roundtrip
@given(from_type(AddRaftVoterRequest))
def test_add_raft_voter_request_roundtrip(instance: AddRaftVoterRequest) -> None:
    writer = entity_writer(AddRaftVoterRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_add_raft_voter_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AddRaftVoterRequest))
def test_add_raft_voter_request_java(
    instance: AddRaftVoterRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
