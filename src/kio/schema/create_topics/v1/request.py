"""
Generated from CreateTopicsRequest.json.
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
class CreatableReplicaAssignment:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    broker_ids: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The brokers to place the partition on."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateableTopicConfig:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The configuration name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The configuration value."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopic:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    num_partitions: i32 = field(metadata={"kafka_type": "int32"})
    """The number of partitions to create in the topic, or -1 if we are either specifying a manual partition assignment or using the default partitions."""
    replication_factor: i16 = field(metadata={"kafka_type": "int16"})
    """The number of replicas to create for each partition in the topic, or -1 if we are either specifying a manual partition assignment or using the default replication factor."""
    assignments: tuple[CreatableReplicaAssignment, ...]
    """The manual partition assignment, or the empty array if we are using automatic assignment."""
    configs: tuple[CreateableTopicConfig, ...]
    """The custom topic configurations to set."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTopicsRequest:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[CreatableTopic, ...]
    """The topics to create."""
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(60000))
    """How long to wait in milliseconds before timing out the request."""
    validate_only: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """If true, check that the topics can be created as specified, but don't create anything."""
