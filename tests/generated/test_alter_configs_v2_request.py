from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_configs.v2.request import AlterableConfig
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


from kio.schema.alter_configs.v2.request import AlterConfigsResource


@given(from_type(AlterConfigsResource))
@settings(max_examples=1)
def test_alter_configs_resource_roundtrip(instance: AlterConfigsResource) -> None:
    writer = entity_writer(AlterConfigsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterConfigsResource))
    assert instance == result


from kio.schema.alter_configs.v2.request import AlterConfigsRequest


@given(from_type(AlterConfigsRequest))
@settings(max_examples=1)
def test_alter_configs_request_roundtrip(instance: AlterConfigsRequest) -> None:
    writer = entity_writer(AlterConfigsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterConfigsRequest))
    assert instance == result
