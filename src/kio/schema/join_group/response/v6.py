"""
Generated from JoinGroupResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupResponseMember:
    __flexible__: ClassVar[bool] = True
    member_id: str = field(metadata={"kafka_type": "string"})
    """The group member ID."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The unique identifier of the consumer instance provided by end user."""
    metadata: bytes = field(metadata={"kafka_type": "bytes"})
    """The group member metadata."""


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    generation_id: int = field(metadata={"kafka_type": "int32"}, default=-1)
    """The generation ID of the group."""
    protocol_name: str = field(metadata={"kafka_type": "string"})
    """The group protocol selected by the coordinator."""
    leader: str = field(metadata={"kafka_type": "string"})
    """The leader of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group coordinator."""
    members: tuple[JoinGroupResponseMember, ...]
