"""
Generated from DeleteRecordsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsPartitionResult:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    low_watermark: i64 = field(metadata={"kafka_type": "int64"})
    """The partition low water mark."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The deletion error code, or 0 if the deletion succeeded."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsTopicResult:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[DeleteRecordsPartitionResult, ...]
    """Each partition that we wanted to delete records from."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[DeleteRecordsTopicResult, ...]
    """Each topic that we wanted to delete records from."""
