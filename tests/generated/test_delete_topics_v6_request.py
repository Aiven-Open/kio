from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_topics.v6.request import DeleteTopicsRequest
from kio.schema.delete_topics.v6.request import DeleteTopicState
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_delete_topic_state: Final = entity_reader(DeleteTopicState)


@given(from_type(DeleteTopicState))
@settings(max_examples=1)
def test_delete_topic_state_roundtrip(instance: DeleteTopicState) -> None:
    writer = entity_writer(DeleteTopicState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_topic_state(buffer)
    assert instance == result


read_delete_topics_request: Final = entity_reader(DeleteTopicsRequest)


@given(from_type(DeleteTopicsRequest))
@settings(max_examples=1)
def test_delete_topics_request_roundtrip(instance: DeleteTopicsRequest) -> None:
    writer = entity_writer(DeleteTopicsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_delete_topics_request(buffer)
    assert instance == result
