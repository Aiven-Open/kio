from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.list_config_resources.v1.response import ConfigResource
from kio.schema.list_config_resources.v1.response import ListConfigResourcesResponse
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_config_resource: Final = entity_reader(ConfigResource)


@pytest.mark.roundtrip
@given(from_type(ConfigResource))
def test_config_resource_roundtrip(instance: ConfigResource) -> None:
    writer = entity_writer(ConfigResource)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_config_resource(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_list_config_resources_response: Final = entity_reader(ListConfigResourcesResponse)


@pytest.mark.roundtrip
@given(from_type(ListConfigResourcesResponse))
def test_list_config_resources_response_roundtrip(
    instance: ListConfigResourcesResponse,
) -> None:
    writer = entity_writer(ListConfigResourcesResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_list_config_resources_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(ListConfigResourcesResponse))
def test_list_config_resources_response_java(
    instance: ListConfigResourcesResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
