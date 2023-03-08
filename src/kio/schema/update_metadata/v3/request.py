"""
Generated from UpdateMetadataRequest.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataPartitionState:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """In older versions of this RPC, the topic name."""
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


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataEndpoint:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
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
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker id."""
    endpoints: tuple[UpdateMetadataEndpoint, ...]
    """The broker endpoints."""
    rack: str | None = field(metadata={"kafka_type": "string"})
    """The rack which this broker belongs to."""


@dataclass(frozen=True, slots=True, kw_only=True)
class UpdateMetadataRequest:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(6)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The controller id."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The controller epoch."""
    ungrouped_partition_states: tuple[UpdateMetadataPartitionState, ...]
    """In older versions of this RPC, each partition that we would like to update."""
    live_brokers: tuple[UpdateMetadataBroker, ...]
