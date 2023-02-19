from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.metadata.v1.request import MetadataRequestTopic
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(MetadataRequestTopic))
@settings(max_examples=1)
def test_metadata_request_topic_roundtrip(instance: MetadataRequestTopic) -> None:
    writer = entity_writer(MetadataRequestTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MetadataRequestTopic))
    assert instance == result


from kio.schema.metadata.v1.request import MetadataRequest


@given(from_type(MetadataRequest))
@settings(max_examples=1)
def test_metadata_request_roundtrip(instance: MetadataRequest) -> None:
    writer = entity_writer(MetadataRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MetadataRequest))
    assert instance == result
