from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.incremental_alter_configs.v0.request import AlterableConfig
from kio.schema.incremental_alter_configs.v0.request import AlterConfigsResource
from kio.schema.incremental_alter_configs.v0.request import (
    IncrementalAlterConfigsRequest,
)
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AlterableConfig))
@settings(max_examples=1)
def test_alterable_config_roundtrip(instance: AlterableConfig) -> None:
    writer = entity_writer(AlterableConfig)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterableConfig))
    assert instance == result


@given(from_type(AlterConfigsResource))
@settings(max_examples=1)
def test_alter_configs_resource_roundtrip(instance: AlterConfigsResource) -> None:
    writer = entity_writer(AlterConfigsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterConfigsResource))
    assert instance == result


@given(from_type(IncrementalAlterConfigsRequest))
@settings(max_examples=1)
def test_incremental_alter_configs_request_roundtrip(
    instance: IncrementalAlterConfigsRequest,
) -> None:
    writer = entity_writer(IncrementalAlterConfigsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(IncrementalAlterConfigsRequest))
    assert instance == result
