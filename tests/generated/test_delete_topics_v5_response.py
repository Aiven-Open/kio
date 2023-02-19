from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.delete_topics.v5.response import DeletableTopicResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(DeletableTopicResult))
@settings(max_examples=1)
def test_deletable_topic_result_roundtrip(instance: DeletableTopicResult) -> None:
    writer = entity_writer(DeletableTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeletableTopicResult))
    assert instance == result


from kio.schema.delete_topics.v5.response import DeleteTopicsResponse


@given(from_type(DeleteTopicsResponse))
@settings(max_examples=1)
def test_delete_topics_response_roundtrip(instance: DeleteTopicsResponse) -> None:
    writer = entity_writer(DeleteTopicsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(DeleteTopicsResponse))
    assert instance == result
