"""
Generated from ``clients/src/main/resources/common/message/StreamsGroupTopologyDescriptionUpdateRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class TopologyDescriptionNode:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(93)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The name of this node (e.g., KSTREAM-SOURCE-0000000000)."""
    node_type: i8 = field(metadata={"kafka_type": "int8"})
    """The type of this node: 1=SOURCE, 2=PROCESSOR, 3=SINK."""
    source_topics: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The source topics this node reads from. Defined only for source nodes, may be empty if source topics are dynamically determined."""
    sink_topic: TopicName | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The topic this node writes to. Defined only for sink nodes, may be null if sink topic is dynamically determined."""
    stores: tuple[str, ...] = field(metadata={"kafka_type": "string"}, default=())
    """The state store names accessed by this node. Defined only for processor nodes."""
    successors: tuple[str, ...] = field(metadata={"kafka_type": "string"}, default=())
    """The names of successor nodes in the processing graph. Predecessor relationships are reconstructed from this field."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopologyDescriptionSubtopology:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(93)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    subtopology_id: str = field(metadata={"kafka_type": "string"})
    """The subtopology identifier, unique within the topology."""
    nodes: tuple[TopologyDescriptionNode, ...]
    """The processing nodes in this subtopology."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopologyDescriptionGlobalStore:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(93)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    source: TopologyDescriptionNode
    """The source node providing data to the global store."""
    processor: TopologyDescriptionNode
    """The processor node that populates the global store."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopologyDescription:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(93)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    subtopologies: tuple[TopologyDescriptionSubtopology, ...]
    """The subtopologies that make up this topology."""
    global_stores: tuple[TopologyDescriptionGlobalStore, ...]
    """Global state stores used by this topology."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StreamsGroupTopologyDescriptionUpdateRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(93)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The streams group identifier."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The ID of the streams group member sending the push. The broker validates that this member is still in the group; mismatches (including when the group itself has been deleted) are rejected with UNKNOWN_MEMBER_ID so the client treats itself as fenced and rejoins."""
    topology_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch of the topology being described."""
    topology_description: TopologyDescription
    """The topology description."""
