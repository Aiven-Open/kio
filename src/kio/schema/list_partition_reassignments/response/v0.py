"""
Generated from ListPartitionReassignmentsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class OngoingPartitionReassignment:
    __flexible__: ClassVar[bool] = True
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The index of the partition."""
    replicas: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The current replica set."""
    adding_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of replicas we are currently adding."""
    removing_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of replicas we are currently removing."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OngoingTopicReassignment:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OngoingPartitionReassignment, ...]
    """The ongoing reassignments for each partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListPartitionReassignmentsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The top-level error code, or 0 if there was no error"""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The top-level error message, or null if there was no error."""
    topics: tuple[OngoingTopicReassignment, ...]
    """The ongoing reassignments for each topic."""
