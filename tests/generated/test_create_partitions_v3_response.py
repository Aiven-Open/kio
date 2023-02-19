from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.create_partitions.v3.response import CreatePartitionsTopicResult
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(CreatePartitionsTopicResult))
@settings(max_examples=1)
def test_create_partitions_topic_result_roundtrip(
    instance: CreatePartitionsTopicResult,
) -> None:
    writer = entity_writer(CreatePartitionsTopicResult)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatePartitionsTopicResult))
    assert instance == result


from kio.schema.create_partitions.v3.response import CreatePartitionsResponse


@given(from_type(CreatePartitionsResponse))
@settings(max_examples=1)
def test_create_partitions_response_roundtrip(
    instance: CreatePartitionsResponse,
) -> None:
    writer = entity_writer(CreatePartitionsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(CreatePartitionsResponse))
    assert instance == result
