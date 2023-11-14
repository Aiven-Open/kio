"""
Generated from AlterPartitionReassignmentsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AlterPartitionReassignmentsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class ReassignablePartitionResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(45)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code for this partition, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message for this partition, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ReassignableTopicResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(45)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[ReassignablePartitionResponse, ...]
    """The responses to partitions to reassign"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterPartitionReassignmentsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(45)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The top-level error message, or null if there was no error."""
    responses: tuple[ReassignableTopicResponse, ...]
    """The responses to topics to reassign."""
