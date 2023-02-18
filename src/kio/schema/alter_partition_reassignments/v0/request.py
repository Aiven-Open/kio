"""
Generated from AlterPartitionReassignmentsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class ReassignablePartition:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    replicas: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The replicas to place the partitions on, or null to cancel a pending reassignment for this partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ReassignableTopic:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[ReassignablePartition, ...]
    """The partitions to reassign."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterPartitionReassignmentsRequest:
    __flexible__: ClassVar[bool] = True
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(60000))
    """The time in ms to wait for the request to complete."""
    topics: tuple[ReassignableTopic, ...]
    """The topics to reassign."""
