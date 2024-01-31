from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_type

from kio.schema.alter_configs.v2.request import AlterableConfig
from kio.schema.alter_configs.v2.request import AlterConfigsRequest
from kio.schema.alter_configs.v2.request import AlterConfigsResource
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_alterable_config: Final = entity_reader(AlterableConfig)


@pytest.mark.roundtrip
@given(from_type(AlterableConfig))
@settings(max_examples=1)
def test_alterable_config_roundtrip(instance: AlterableConfig) -> None:
    writer = entity_writer(AlterableConfig)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alterable_config(buffer)
    assert instance == result


read_alter_configs_resource: Final = entity_reader(AlterConfigsResource)


@pytest.mark.roundtrip
@given(from_type(AlterConfigsResource))
@settings(max_examples=1)
def test_alter_configs_resource_roundtrip(instance: AlterConfigsResource) -> None:
    writer = entity_writer(AlterConfigsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_configs_resource(buffer)
    assert instance == result


read_alter_configs_request: Final = entity_reader(AlterConfigsRequest)


@pytest.mark.roundtrip
@given(from_type(AlterConfigsRequest))
@settings(max_examples=1)
def test_alter_configs_request_roundtrip(instance: AlterConfigsRequest) -> None:
    writer = entity_writer(AlterConfigsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_configs_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(AlterConfigsRequest))
def test_alter_configs_request_java(
    instance: AlterConfigsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
