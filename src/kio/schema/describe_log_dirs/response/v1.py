"""
Generated from DescribeLogDirsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsPartition:
    __flexible__: ClassVar[bool] = False
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    partition_size: i64 = field(metadata={"kafka_type": "int64"})
    """The size of the log segments in this partition in bytes."""
    offset_lag: i64 = field(metadata={"kafka_type": "int64"})
    """The lag of the log's LEO w.r.t. partition's HW (if it is the current log for the partition) or current replica's LEO (if it is the future log for the partition)"""
    is_future_key: bool = field(metadata={"kafka_type": "bool"})
    """True if this log is created by AlterReplicaLogDirsRequest and will replace the current log of the replica in the future."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[DescribeLogDirsPartition, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsResult:
    __flexible__: ClassVar[bool] = False
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    log_dir: str = field(metadata={"kafka_type": "string"})
    """The absolute log directory path."""
    topics: tuple[DescribeLogDirsTopic, ...]
    """Each topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[DescribeLogDirsResult, ...]
    """The log directories."""
