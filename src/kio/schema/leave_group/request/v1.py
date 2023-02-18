"""
Generated from LeaveGroupRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.types import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaveGroupRequest:
    __flexible__: ClassVar[bool] = False
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The ID of the group to leave."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID to remove from the group."""
