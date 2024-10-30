from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.create_topics.v1.request import CreatableReplicaAssignment
from kio.schema.create_topics.v1.request import CreatableTopic
from kio.schema.create_topics.v1.request import CreatableTopicConfig
from kio.schema.create_topics.v1.request import CreateTopicsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_creatable_replica_assignment: Final = entity_reader(CreatableReplicaAssignment)


@pytest.mark.roundtrip
@given(from_type(CreatableReplicaAssignment))
def test_creatable_replica_assignment_roundtrip(
    instance: CreatableReplicaAssignment,
) -> None:
    writer = entity_writer(CreatableReplicaAssignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_creatable_replica_assignment(buffer)
    assert instance == result


read_creatable_topic_config: Final = entity_reader(CreatableTopicConfig)


@pytest.mark.roundtrip
@given(from_type(CreatableTopicConfig))
def test_creatable_topic_config_roundtrip(instance: CreatableTopicConfig) -> None:
    writer = entity_writer(CreatableTopicConfig)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_creatable_topic_config(buffer)
    assert instance == result


read_creatable_topic: Final = entity_reader(CreatableTopic)


@pytest.mark.roundtrip
@given(from_type(CreatableTopic))
def test_creatable_topic_roundtrip(instance: CreatableTopic) -> None:
    writer = entity_writer(CreatableTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_creatable_topic(buffer)
    assert instance == result


read_create_topics_request: Final = entity_reader(CreateTopicsRequest)


@pytest.mark.roundtrip
@given(from_type(CreateTopicsRequest))
def test_create_topics_request_roundtrip(instance: CreateTopicsRequest) -> None:
    writer = entity_writer(CreateTopicsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_topics_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(CreateTopicsRequest))
def test_create_topics_request_java(
    instance: CreateTopicsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
