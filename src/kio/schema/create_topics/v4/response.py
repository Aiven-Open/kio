"""
Generated from CreateTopicsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/CreateTopicsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class CreatableTopicResult:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateTopicsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(19)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[CreatableTopicResult, ...]
    """Results for each topic we tried to create."""
