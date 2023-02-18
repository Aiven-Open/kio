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
    __flexible__: ClassVar[bool] = False
    member_id: str = field(metadata={"kafka_type": "string"})
    """The ID of the member to assign."""
    assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The member assignment."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupRequest:
    __flexible__: ClassVar[bool] = False
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The generation of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group."""
    assignments: tuple[SyncGroupRequestAssignment, ...]
    """Each assignment."""
