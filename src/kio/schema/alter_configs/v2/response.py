"""
Generated from AlterConfigsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AlterConfigsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsResourceResponse:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(33)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The resource error code."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The resource error message, or null if there was no error."""
    resource_type: i8 = field(metadata={"kafka_type": "int8"})
    """The resource type."""
    resource_name: str = field(metadata={"kafka_type": "string"})
    """The resource name."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterConfigsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(33)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    responses: tuple[AlterConfigsResourceResponse, ...]
    """The responses for each resource."""
