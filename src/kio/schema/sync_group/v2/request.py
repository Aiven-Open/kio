"""
Generated from ``clients/src/main/resources/common/message/SyncGroupRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupRequestAssignment:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(14)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The ID of the member to assign."""
    assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The member assignment."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(14)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The generation of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group."""
    assignments: tuple[SyncGroupRequestAssignment, ...]
    """Each assignment."""
