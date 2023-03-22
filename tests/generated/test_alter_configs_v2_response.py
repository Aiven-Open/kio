from __future__ import annotations

from typing import Final

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_configs.v2.response import AlterConfigsResourceResponse
from kio.schema.alter_configs.v2.response import AlterConfigsResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import setup_buffer

read_alter_configs_resource_response: Final = entity_reader(
    AlterConfigsResourceResponse
)


@given(from_type(AlterConfigsResourceResponse))
@settings(max_examples=1)
def test_alter_configs_resource_response_roundtrip(
    instance: AlterConfigsResourceResponse,
) -> None:
    writer = entity_writer(AlterConfigsResourceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_configs_resource_response(buffer)
    assert instance == result


read_alter_configs_response: Final = entity_reader(AlterConfigsResponse)


@given(from_type(AlterConfigsResponse))
@settings(max_examples=1)
def test_alter_configs_response_roundtrip(instance: AlterConfigsResponse) -> None:
    writer = entity_writer(AlterConfigsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_configs_response(buffer)
    assert instance == result
