"""
Generated from ListPartitionReassignmentsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class ListPartitionReassignmentsTopics:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partition_indexes: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The partitions to list partition reassignments for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListPartitionReassignmentsRequest:
    __flexible__: ClassVar[bool] = True
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(60000))
    """The time in ms to wait for the request to complete."""
    topics: tuple[ListPartitionReassignmentsTopics, ...]
    """The topics to list partition reassignments for, or null to list everything."""
