from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.update_raft_voter.v0.request import KRaftVersionFeature
from kio.schema.update_raft_voter.v0.request import Listener
from kio.schema.update_raft_voter.v0.request import UpdateRaftVoterRequest
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


read_k_raft_version_feature: Final = entity_reader(KRaftVersionFeature)


@pytest.mark.roundtrip
@given(from_type(KRaftVersionFeature))
def test_k_raft_version_feature_roundtrip(instance: KRaftVersionFeature) -> None:
    writer = entity_writer(KRaftVersionFeature)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_k_raft_version_feature(buffer)
    assert instance == result


read_update_raft_voter_request: Final = entity_reader(UpdateRaftVoterRequest)


@pytest.mark.roundtrip
@given(from_type(UpdateRaftVoterRequest))
def test_update_raft_voter_request_roundtrip(instance: UpdateRaftVoterRequest) -> None:
    writer = entity_writer(UpdateRaftVoterRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_update_raft_voter_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(UpdateRaftVoterRequest))
def test_update_raft_voter_request_java(
    instance: UpdateRaftVoterRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
