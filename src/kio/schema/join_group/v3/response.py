"""
Generated from JoinGroupResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/JoinGroupResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupResponseMember:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(11)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The group member ID."""
    metadata: bytes = field(metadata={"kafka_type": "bytes"})
    """The group member metadata."""


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(11)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The generation ID of the group."""
    protocol_name: str = field(metadata={"kafka_type": "string"})
    """The group protocol selected by the coordinator."""
    leader: str = field(metadata={"kafka_type": "string"})
    """The leader of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group coordinator."""
    members: tuple[JoinGroupResponseMember, ...]
