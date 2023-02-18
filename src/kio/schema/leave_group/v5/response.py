"""
Generated from LeaveGroupResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class MemberResponse:
    __flexible__: ClassVar[bool] = True
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID to remove from the group."""
    group_instance_id: str | None = field(metadata={"kafka_type": "string"})
    """The group instance ID to remove from the group."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaveGroupResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    members: tuple[MemberResponse, ...]
    """List of leaving member responses."""
