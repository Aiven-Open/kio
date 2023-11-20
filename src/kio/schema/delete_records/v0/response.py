"""
Generated from DeleteRecordsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DeleteRecordsResponse.json
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
class DeleteRecordsPartitionResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(21)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    low_watermark: i64 = field(metadata={"kafka_type": "int64"})
    """The partition low water mark."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The deletion error code, or 0 if the deletion succeeded."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsTopicResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(21)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[DeleteRecordsPartitionResult, ...]
    """Each partition that we wanted to delete records from."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(21)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[DeleteRecordsTopicResult, ...]
    """Each topic that we wanted to delete records from."""
