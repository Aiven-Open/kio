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
    topics: tuple[OffsetForLeaderTopicResult, ...]
    """Each topic we fetched offsets for."""
