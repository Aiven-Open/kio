from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_topics.v0.response import CreatableTopicResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(CreatableTopicResult))
@settings(max_examples=1)
def test_creatable_topic_result_roundtrip(instance: CreatableTopicResult) -> None:
    writer = entity_writer(CreatableTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatableTopicResult))
    assert instance == result


from kio.schema.create_topics.v0.response import CreateTopicsResponse


@given(from_type(CreateTopicsResponse))
@settings(max_examples=1)
def test_create_topics_response_roundtrip(instance: CreateTopicsResponse) -> None:
    writer = entity_writer(CreateTopicsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreateTopicsResponse))
    assert instance == result
