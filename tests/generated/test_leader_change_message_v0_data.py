from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.leader_change_message.v0.data import Voter
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(Voter))
@settings(max_examples=1)
def test_voter_roundtrip(instance: Voter) -> None:
    writer = entity_writer(Voter)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(Voter))
    assert instance == result


from kio.schema.leader_change_message.v0.data import LeaderChangeMessage


@given(from_type(LeaderChangeMessage))
@settings(max_examples=1)
def test_leader_change_message_roundtrip(instance: LeaderChangeMessage) -> None:
    writer = entity_writer(LeaderChangeMessage)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(LeaderChangeMessage))
    assert instance == result
