from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_configs.v2.response import AlterConfigsResourceResponse
from kio.serial import entity_decoder
from kio.serial import entity_writer
from kio.serial import read_sync
from tests.conftest import setup_buffer


@given(from_type(AlterConfigsResourceResponse))
@settings(max_examples=1)
def test_alter_configs_resource_response_roundtrip(
    instance: AlterConfigsResourceResponse,
) -> None:
    writer = entity_writer(AlterConfigsResourceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterConfigsResourceResponse))
    assert instance == result


from kio.schema.alter_configs.v2.response import AlterConfigsResponse


@given(from_type(AlterConfigsResponse))
@settings(max_examples=1)
def test_alter_configs_response_roundtrip(instance: AlterConfigsResponse) -> None:
    writer = entity_writer(AlterConfigsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_sync(buffer, entity_decoder(AlterConfigsResponse))
    assert instance == result
