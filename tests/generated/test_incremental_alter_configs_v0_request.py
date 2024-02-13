from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.incremental_alter_configs.v0.request import AlterableConfig
from kio.schema.incremental_alter_configs.v0.request import AlterConfigsResource
from kio.schema.incremental_alter_configs.v0.request import (
    IncrementalAlterConfigsRequest,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_alterable_config: Final = entity_reader(AlterableConfig)


@pytest.mark.roundtrip
@given(from_type(AlterableConfig))
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
def test_alter_configs_resource_roundtrip(instance: AlterConfigsResource) -> None:
    writer = entity_writer(AlterConfigsResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_alter_configs_resource(buffer)
    assert instance == result


read_incremental_alter_configs_request: Final = entity_reader(
    IncrementalAlterConfigsRequest
)


@pytest.mark.roundtrip
@given(from_type(IncrementalAlterConfigsRequest))
def test_incremental_alter_configs_request_roundtrip(
    instance: IncrementalAlterConfigsRequest,
) -> None:
    writer = entity_writer(IncrementalAlterConfigsRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        buffer.seek(0)
        result = read_incremental_alter_configs_request(buffer)
    assert instance == result


@pytest.mark.java
@given(instance=from_type(IncrementalAlterConfigsRequest))
def test_incremental_alter_configs_request_java(
    instance: IncrementalAlterConfigsRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
