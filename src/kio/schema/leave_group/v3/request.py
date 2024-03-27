"""
Generated from ``clients/src/main/resources/common/message/LeaveGroupRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16


@dataclass(frozen=True, slots=True, kw_only=True)
class MemberIdentity:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(13)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID to remove from the group."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The group instance ID to remove from the group."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaveGroupRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(13)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The ID of the group to leave."""
    members: tuple[MemberIdentity, ...]
    """List of leaving member identities."""
