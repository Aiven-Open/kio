"""
Generated from DescribeLogDirsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeLogDirsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsPartition:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(35)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
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
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(35)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[DescribeLogDirsPartition, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsResult:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(35)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    log_dir: str = field(metadata={"kafka_type": "string"})
    """The absolute log directory path."""
    topics: tuple[DescribeLogDirsTopic, ...]
    """Each topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(35)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results: tuple[DescribeLogDirsResult, ...]
    """The log directories."""
