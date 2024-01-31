from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_topics.v6.request import CreatableReplicaAssignment
from kio.schema.create_topics.v6.request import CreatableTopic
from kio.schema.create_topics.v6.request import CreateableTopicConfig
from kio.schema.create_topics.v6.request import CreateTopicsRequest
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_creatable_replica_assignment: Final = entity_reader(CreatableReplicaAssignment)


@pytest.mark.roundtrip
@given(from_type(CreatableReplicaAssignment))
@settings(max_examples=1)
def test_creatable_replica_assignment_roundtrip(
    instance: CreatableReplicaAssignment,
) -> None:
    writer = entity_writer(CreatableReplicaAssignment)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_creatable_replica_assignment(buffer)
    assert instance == result


read_createable_topic_config: Final = entity_reader(CreateableTopicConfig)


@pytest.mark.roundtrip
@given(from_type(CreateableTopicConfig))
@settings(max_examples=1)
def test_createable_topic_config_roundtrip(instance: CreateableTopicConfig) -> None:
    writer = entity_writer(CreateableTopicConfig)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_createable_topic_config(buffer)
    assert instance == result


read_creatable_topic: Final = entity_reader(CreatableTopic)


@pytest.mark.roundtrip
@given(from_type(CreatableTopic))
@settings(max_examples=1)
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
@settings(max_examples=1)
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
