from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leader_change_message.v0.data import LeaderChangeMessage
from kio.schema.leader_change_message.v0.data import Voter
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_voter: Final = entity_reader(Voter)


@pytest.mark.roundtrip
@given(from_type(Voter))
@settings(max_examples=1)
def test_voter_roundtrip(instance: Voter) -> None:
    writer = entity_writer(Voter)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_voter(buffer)
    assert instance == result


read_leader_change_message: Final = entity_reader(LeaderChangeMessage)


@pytest.mark.roundtrip
@given(from_type(LeaderChangeMessage))
@settings(max_examples=1)
def test_leader_change_message_roundtrip(instance: LeaderChangeMessage) -> None:
    writer = entity_writer(LeaderChangeMessage)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_leader_change_message(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(LeaderChangeMessage))
def test_leader_change_message_java(
    instance: LeaderChangeMessage, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
