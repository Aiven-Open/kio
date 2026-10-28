from __future__ import annotations

from typing import Final

import pytest

from hypothesis import given
from hypothesis.strategies import from_type

from kio.schema.streams_group_topology_description_update.v0.request import (
    StreamsGroupTopologyDescriptionUpdateRequest,
)
from kio.schema.streams_group_topology_description_update.v0.request import (
    TopologyDescription,
)
from kio.schema.streams_group_topology_description_update.v0.request import (
    TopologyDescriptionGlobalStore,
)
from kio.schema.streams_group_topology_description_update.v0.request import (
    TopologyDescriptionNode,
)
from kio.schema.streams_group_topology_description_update.v0.request import (
    TopologyDescriptionSubtopology,
)
from kio.serial import entity_reader
from kio.serial import entity_writer
from tests.conftest import JavaTester
from tests.conftest import setup_buffer

read_topology_description_node: Final = entity_reader(TopologyDescriptionNode)


@pytest.mark.roundtrip
@given(from_type(TopologyDescriptionNode))
def test_topology_description_node_roundtrip(instance: TopologyDescriptionNode) -> None:
    writer = entity_writer(TopologyDescriptionNode)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_topology_description_node(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_topology_description_subtopology: Final = entity_reader(
    TopologyDescriptionSubtopology
)


@pytest.mark.roundtrip
@given(from_type(TopologyDescriptionSubtopology))
def test_topology_description_subtopology_roundtrip(
    instance: TopologyDescriptionSubtopology,
) -> None:
    writer = entity_writer(TopologyDescriptionSubtopology)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_topology_description_subtopology(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_topology_description_global_store: Final = entity_reader(
    TopologyDescriptionGlobalStore
)


@pytest.mark.roundtrip
@given(from_type(TopologyDescriptionGlobalStore))
def test_topology_description_global_store_roundtrip(
    instance: TopologyDescriptionGlobalStore,
) -> None:
    writer = entity_writer(TopologyDescriptionGlobalStore)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_topology_description_global_store(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_topology_description: Final = entity_reader(TopologyDescription)


@pytest.mark.roundtrip
@given(from_type(TopologyDescription))
def test_topology_description_roundtrip(instance: TopologyDescription) -> None:
    writer = entity_writer(TopologyDescription)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_topology_description(
            buffer.getvalue(),
            0,
        )

    assert instance == result


read_streams_group_topology_description_update_request: Final = entity_reader(
    StreamsGroupTopologyDescriptionUpdateRequest
)


@pytest.mark.roundtrip
@given(from_type(StreamsGroupTopologyDescriptionUpdateRequest))
def test_streams_group_topology_description_update_request_roundtrip(
    instance: StreamsGroupTopologyDescriptionUpdateRequest,
) -> None:
    writer = entity_writer(StreamsGroupTopologyDescriptionUpdateRequest)
    with setup_buffer() as buffer:
        writer(buffer, instance)
        result, _ = read_streams_group_topology_description_update_request(
            buffer.getvalue(),
            0,
        )

    assert instance == result


@pytest.mark.java
@given(instance=from_type(StreamsGroupTopologyDescriptionUpdateRequest))
def test_streams_group_topology_description_update_request_java(
    instance: StreamsGroupTopologyDescriptionUpdateRequest, java_tester: JavaTester
) -> None:
    java_tester.test(instance)
