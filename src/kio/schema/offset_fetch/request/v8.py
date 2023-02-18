"""
Generated from OffsetFetchRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import GroupId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequestTopics:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_indexes: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The partition indexes we would like to fetch offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequestGroup:
    __flexible__: ClassVar[bool] = True
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID."""
    topics: tuple[OffsetFetchRequestTopics, ...]
    """Each topic we would like to fetch offsets for, or null to fetch offsets for all topics."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchRequest:
    __flexible__: ClassVar[bool] = True
    groups: tuple[OffsetFetchRequestGroup, ...]
    """Each group we would like to fetch offsets for"""
    require_stable: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """Whether broker should hold on returning unstable offsets but set a retriable error code for the partitions."""
