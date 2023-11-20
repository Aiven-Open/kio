"""
Generated from SyncGroupResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/SyncGroupResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(14)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    protocol_type: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The group protocol type."""
    protocol_name: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The group protocol name."""
    assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The member assignment."""
