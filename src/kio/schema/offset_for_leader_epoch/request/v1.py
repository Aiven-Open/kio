"""
Generated from OffsetForLeaderEpochRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderPartition:
    __flexible__: ClassVar[bool] = False
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch to look up an offset for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderTopic:
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetForLeaderPartition, ...]
    """Each partition to get offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderEpochRequest:
    __flexible__: ClassVar[bool] = False
    topics: tuple[OffsetForLeaderTopic, ...]
    """Each topic to get offsets for."""
