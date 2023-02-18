"""
Generated from OffsetForLeaderEpochResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class EpochEndOffset:
    __flexible__: ClassVar[bool] = False
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code 0, or if there was no error."""
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The leader epoch of the partition."""
    end_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The end offset of the epoch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderTopicResult:
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[EpochEndOffset, ...]
    """Each partition in the topic we fetched offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderEpochResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[OffsetForLeaderTopicResult, ...]
    """Each topic we fetched offsets for."""
