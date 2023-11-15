from __future__ import annotations

from typing import Final

import pytest
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_topics.v6.response import CreatableTopicConfigs
from kio.schema.create_topics.v6.response import CreatableTopicResult
from kio.schema.create_topics.v6.response import CreateTopicsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_creatable_topic_configs: Final = entity_reader(CreatableTopicConfigs)


@pytest.mark.roundtrip
@given(from_type(CreatableTopicConfigs))
@settings(max_examples=1)
def test_creatable_topic_configs_roundtrip(instance: CreatableTopicConfigs) -> None:
    writer = entity_writer(CreatableTopicConfigs)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_creatable_topic_configs(buffer)
    assert instance == result


read_creatable_topic_result: Final = entity_reader(CreatableTopicResult)


@pytest.mark.roundtrip
@given(from_type(CreatableTopicResult))
@settings(max_examples=1)
def test_creatable_topic_result_roundtrip(instance: CreatableTopicResult) -> None:
    writer = entity_writer(CreatableTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_creatable_topic_result(buffer)
    assert instance == result


read_create_topics_response: Final = entity_reader(CreateTopicsResponse)


@pytest.mark.roundtrip
@given(from_type(CreateTopicsResponse))
@settings(max_examples=1)
def test_create_topics_response_roundtrip(instance: CreateTopicsResponse) -> None:
    writer = entity_writer(CreateTopicsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_create_topics_response(buffer)
    assert instance == result
