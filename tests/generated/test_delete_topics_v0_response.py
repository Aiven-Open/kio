from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.delete_topics.v0.response import DeletableTopicResult
from kio.schema.delete_topics.v0.response import DeleteTopicsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_deletable_topic_result: Final = entity_reader(DeletableTopicResult)


@pytest.mark.roundtrip
@given(from_type(DeletableTopicResult))
def test_deletable_topic_result_roundtrip(instance: DeletableTopicResult) -> None:
    writer = entity_writer(DeletableTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_deletable_topic_result(buffer)
    assert instance == result


read_delete_topics_response: Final = entity_reader(DeleteTopicsResponse)


@pytest.mark.roundtrip
@given(from_type(DeleteTopicsResponse))
def test_delete_topics_response_roundtrip(instance: DeleteTopicsResponse) -> None:
    writer = entity_writer(DeleteTopicsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_topics_response(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(DeleteTopicsResponse))
def test_delete_topics_response_java(
    instance: DeleteTopicsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
