"""
Generated from DescribeGroupsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedGroupMember:
    __flexible__: ClassVar[bool] = True
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group coordinator."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The unique identifier of the consumer instance provided by end user."""
    client_id: str = field(metadata={"kafka_type": "string"})
    """The client ID used in the member's latest join group request."""
    client_host: str = field(metadata={"kafka_type": "string"})
    """The client host."""
    member_metadata: bytes = field(metadata={"kafka_type": "bytes"})
    """The metadata corresponding to the current group protocol in use."""
    member_assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The current assignment provided by the group leader."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedGroup:
    __flexible__: ClassVar[bool] = True
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The describe error, or 0 if there was no error."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID string."""
    group_state: str = field(metadata={"kafka_type": "string"})
    """The group state string, or the empty string."""
    protocol_type: str = field(metadata={"kafka_type": "string"})
    """The group protocol type, or the empty string."""
    protocol_data: str = field(metadata={"kafka_type": "string"})
    """The group protocol data, or the empty string."""
    members: tuple[DescribedGroupMember, ...]
    """The group members."""
    authorized_operations: int = field(
        metadata={"kafka_type": "int32"}, default=-2147483648
    )
    """32-bit bitfield to represent authorized operations for this group."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeGroupsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    groups: tuple[DescribedGroup, ...]
    """Each described group."""
