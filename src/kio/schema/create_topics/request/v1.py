"""
Generated from CreateTopicsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableReplicaAssignment:
    __flexible__: ClassVar[bool] = False
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    broker_ids: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The brokers to place the partition on."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateableTopicConfig:
    __flexible__: ClassVar[bool] = False
    name: str = field(metadata={"kafka_type": "string"})
    """The configuration name."""
    value: str | None = field(metadata={"kafka_type": "string"})
    """The configuration value."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopic:
    __flexible__: ClassVar[bool] = False
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
    __flexible__: ClassVar[bool] = False
    topics: tuple[CreatableTopic, ...]
    """The topics to create."""
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(60000))
    """How long to wait in milliseconds before timing out the request."""
    validate_only: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """If true, check that the topics can be created as specified, but don't create anything."""
