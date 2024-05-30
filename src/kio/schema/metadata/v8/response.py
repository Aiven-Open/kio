"""
Generated from ``clients/src/main/resources/common/message/MetadataResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataResponseBroker:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    node_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID."""
    host: str = field(metadata={"kafka_type": "string"})
    """The broker hostname."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The broker port."""
    rack: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The rack of the broker, or null if it has not been assigned to a rack."""


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataResponsePartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition error, or 0 if there was no error."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the leader broker."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The leader epoch of this partition."""
    replica_nodes: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of all nodes that host this partition."""
    isr_nodes: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of nodes that are in sync with the leader for this partition."""
    offline_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of offline replicas of this partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataResponseTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The topic error, or 0 if there was no error."""
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    is_internal: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if the topic is internal."""
    partitions: tuple[MetadataResponsePartition, ...]
    """Each partition in the topic."""
    topic_authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class MetadataResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(3)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    brokers: tuple[MetadataResponseBroker, ...]
    """Each broker in the response."""
    cluster_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The cluster ID that responding broker belongs to."""
    controller_id: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(-1)
    )
    """The ID of the controller broker."""
    topics: tuple[MetadataResponseTopic, ...]
    """Each topic in the response."""
    cluster_authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this cluster."""
