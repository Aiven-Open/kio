"""
Generated from ListOffsetsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsPartitionResponse:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The partition error code, or 0 if there was no error."""
    timestamp: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The timestamp associated with the returned offset."""
    offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The returned offset."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopicResponse:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[ListOffsetsPartitionResponse, ...]
    """Each partition in the response."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[ListOffsetsTopicResponse, ...]
    """Each topic in the response."""
