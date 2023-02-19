from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.update_metadata.v1.request import UpdateMetadataPartitionState
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(UpdateMetadataPartitionState))
@settings(max_examples=1)
def test_update_metadata_partition_state_roundtrip(
    instance: UpdateMetadataPartitionState,
) -> None:
    writer = entity_writer(UpdateMetadataPartitionState)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdateMetadataPartitionState))
    assert instance == result


from kio.schema.update_metadata.v1.request import UpdateMetadataEndpoint


@given(from_type(UpdateMetadataEndpoint))
@settings(max_examples=1)
def test_update_metadata_endpoint_roundtrip(instance: UpdateMetadataEndpoint) -> None:
    writer = entity_writer(UpdateMetadataEndpoint)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdateMetadataEndpoint))
    assert instance == result


from kio.schema.update_metadata.v1.request import UpdateMetadataBroker


@given(from_type(UpdateMetadataBroker))
@settings(max_examples=1)
def test_update_metadata_broker_roundtrip(instance: UpdateMetadataBroker) -> None:
    writer = entity_writer(UpdateMetadataBroker)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdateMetadataBroker))
    assert instance == result


from kio.schema.update_metadata.v1.request import UpdateMetadataRequest


@given(from_type(UpdateMetadataRequest))
@settings(max_examples=1)
def test_update_metadata_request_roundtrip(instance: UpdateMetadataRequest) -> None:
    writer = entity_writer(UpdateMetadataRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(UpdateMetadataRequest))
    assert instance == result
