from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.streams_group_topology_description_update.v0.response import (
    StreamsGroupTopologyDescriptionUpdateResponse,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_streams_group_topology_description_update_response: Final = entity_reader(
    StreamsGroupTopologyDescriptionUpdateResponse
)


@pytest.mark.roundtrip
@given(from_type(StreamsGroupTopologyDescriptionUpdateResponse))
def test_streams_group_topology_description_update_response_roundtrip(
    instance: StreamsGroupTopologyDescriptionUpdateResponse,
) -> None:
    writer = entity_writer(StreamsGroupTopologyDescriptionUpdateResponse)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_streams_group_topology_description_update_response(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(StreamsGroupTopologyDescriptionUpdateResponse))
def test_streams_group_topology_description_update_response_java(
    instance: StreamsGroupTopologyDescriptionUpdateResponse, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
