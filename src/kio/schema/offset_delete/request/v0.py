"""
Generated from OffsetDeleteRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId
from kio.schema.entity import TopicName
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetDeleteRequestPartition:
    __flexible__: ClassVar[bool] = False
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetDeleteRequestTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetDeleteRequestPartition, ...]
    """Each partition to delete offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetDeleteRequest:
    __flexible__: ClassVar[bool] = False
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
    topics: tuple[OffsetDeleteRequestTopic, ...]
    """The topics to delete offsets for"""
