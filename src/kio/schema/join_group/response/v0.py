"""
Generated from JoinGroupResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupResponseMember:
    __flexible__: ClassVar[bool] = False
    member_id: str = field(metadata={"kafka_type": "string"})
    """The group member ID."""
    metadata: bytes = field(metadata={"kafka_type": "bytes"})
    """The group member metadata."""


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupResponse:
    __flexible__: ClassVar[bool] = False
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
