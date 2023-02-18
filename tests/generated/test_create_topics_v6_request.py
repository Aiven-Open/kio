from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_topics.v6.request import CreatableReplicaAssignment
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(CreatableReplicaAssignment))
@settings(max_examples=1)
def test_creatable_replica_assignment_roundtrip(
    instance: CreatableReplicaAssignment,
) -> None:
    writer = entity_writer(CreatableReplicaAssignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatableReplicaAssignment))
    assert instance == result


from kio.schema.create_topics.v6.request import CreateableTopicConfig


@given(from_type(CreateableTopicConfig))
@settings(max_examples=1)
def test_createable_topic_config_roundtrip(instance: CreateableTopicConfig) -> None:
    writer = entity_writer(CreateableTopicConfig)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreateableTopicConfig))
    assert instance == result


from kio.schema.create_topics.v6.request import CreatableTopic


@given(from_type(CreatableTopic))
@settings(max_examples=1)
def test_creatable_topic_roundtrip(instance: CreatableTopic) -> None:
    writer = entity_writer(CreatableTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatableTopic))
    assert instance == result


from kio.schema.create_topics.v6.request import CreateTopicsRequest


@given(from_type(CreateTopicsRequest))
@settings(max_examples=1)
def test_create_topics_request_roundtrip(instance: CreateTopicsRequest) -> None:
    writer = entity_writer(CreateTopicsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreateTopicsRequest))
    assert instance == result
