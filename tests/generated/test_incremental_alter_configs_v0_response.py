from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.incremental_alter_configs.v0.response import (
    AlterConfigsResourceResponse,
)
from kio.schema.incremental_alter_configs.v0.response import (
    IncrementalAlterConfigsResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_alter_configs_resource_response: Final = entity_reader(
    AlterConfigsResourceResponse
)


@pytest.mark.roundtrip
@given(from_type(AlterConfigsResourceResponse))
def test_alter_configs_resource_response_roundtrip(
    instance: AlterConfigsResourceResponse,
) -> None:
    writer = entity_writer(AlterConfigsResourceResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_alter_configs_resource_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_incremental_alter_configs_response: Final = entity_reader(
    IncrementalAlterConfigsResponse
)


@pytest.mark.roundtrip
@given(from_type(IncrementalAlterConfigsResponse))
def test_incremental_alter_configs_response_roundtrip(
    instance: IncrementalAlterConfigsResponse,
) -> None:
    writer = entity_writer(IncrementalAlterConfigsResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_incremental_alter_configs_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(IncrementalAlterConfigsResponse))
def test_incremental_alter_configs_response_java(
    instance: IncrementalAlterConfigsResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
