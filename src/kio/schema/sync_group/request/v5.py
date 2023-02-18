"""
Generated from SyncGroupRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupRequestAssignment:
    __flexible__: ClassVar[bool] = True
    member_id: str = field(metadata={"kafka_type": "string"})
    """The ID of the member to assign."""
    assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The member assignment."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupRequest:
    __flexible__: ClassVar[bool] = True
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The generation of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The unique identifier of the consumer instance provided by end user."""
    protocol_type: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The group protocol type."""
    protocol_name: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The group protocol name."""
    assignments: tuple[SyncGroupRequestAssignment, ...]
    """Each assignment."""
