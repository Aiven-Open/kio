"""
Generated from DeleteRecordsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsPartitionResult:
    __flexible__: ClassVar[bool] = True
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    low_watermark: int = field(metadata={"kafka_type": "int64"})
    """The partition low water mark."""
    error_code: int = field(metadata={"kafka_type": "int16"})
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
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[DeleteRecordsTopicResult, ...]
    """Each topic that we wanted to delete records from."""
