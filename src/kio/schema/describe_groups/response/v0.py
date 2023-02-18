"""
Generated from DescribeGroupsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.types import GroupId


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedGroupMember:
    __flexible__: ClassVar[bool] = False
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group coordinator."""
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
    __flexible__: ClassVar[bool] = False
    error_code: i16 = field(metadata={"kafka_type": "int16"})
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


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeGroupsResponse:
    __flexible__: ClassVar[bool] = False
    groups: tuple[DescribedGroup, ...]
    """Each described group."""
