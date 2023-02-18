from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.metadata.v0.response import MetadataResponseBroker
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(MetadataResponseBroker))
@settings(max_examples=1)
def test_metadata_response_broker_roundtrip(instance: MetadataResponseBroker) -> None:
    writer = entity_writer(MetadataResponseBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MetadataResponseBroker))
    assert instance == result


from kio.schema.metadata.v0.response import MetadataResponsePartition


@given(from_type(MetadataResponsePartition))
@settings(max_examples=1)
def test_metadata_response_partition_roundtrip(
    instance: MetadataResponsePartition,
) -> None:
    writer = entity_writer(MetadataResponsePartition)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MetadataResponsePartition))
    assert instance == result


from kio.schema.metadata.v0.response import MetadataResponseTopic


@given(from_type(MetadataResponseTopic))
@settings(max_examples=1)
def test_metadata_response_topic_roundtrip(instance: MetadataResponseTopic) -> None:
    writer = entity_writer(MetadataResponseTopic)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MetadataResponseTopic))
    assert instance == result


from kio.schema.metadata.v0.response import MetadataResponse


@given(from_type(MetadataResponse))
@settings(max_examples=1)
def test_metadata_response_roundtrip(instance: MetadataResponse) -> None:
    writer = entity_writer(MetadataResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(MetadataResponse))
    assert instance == result
