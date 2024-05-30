"""
Generated from ``clients/src/main/resources/common/message/LeaveGroupResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class MemberResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(13)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID to remove from the group."""
    group_instance_id: str | None = field(metadata={"kafka_type": "string"})
    """The group instance ID to remove from the group."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaveGroupResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(13)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    members: tuple[MemberResponse, ...]
    """List of leaving member responses."""
