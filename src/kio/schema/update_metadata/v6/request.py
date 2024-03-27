"""
Generated from ``clients/src/main/resources/common/message/UpdateMetadataRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataPartitionState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The controller epoch."""
    leader: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the broker which is the current partition leader."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The leader epoch of this partition."""
    isr: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The brokers which are in the ISR for this partition."""
    zk_version: i32 = field(metadata={"kafka_type": "int32"})
    """The Zookeeper version."""
    replicas: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """All the replicas of this partition."""
    offline_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The replicas of this partition which are offline."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataTopicState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_states: tuple[UpdateMetadataPartitionState, ...]
    """The partition that we would like to update."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataEndpoint:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The port of this endpoint"""
    host: str = field(metadata={"kafka_type": "string"})
    """The hostname of this endpoint"""
    listener: str = field(metadata={"kafka_type": "string"})
    """The listener name."""
    security_protocol: i16 = field(metadata={"kafka_type": "int16"})
    """The security protocol type."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataBroker:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    id_: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker id."""
    endpoints: tuple[UpdateMetadataEndpoint, ...]
    """The broker endpoints."""
    rack: str | None = field(metadata={"kafka_type": "string"})
    """The rack which this broker belongs to."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The controller id."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The controller epoch."""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The broker epoch."""
    topic_states: tuple[UpdateMetadataTopicState, ...]
    """In newer versions of this RPC, each topic that we would like to update."""
    live_brokers: tuple[UpdateMetadataBroker, ...]
