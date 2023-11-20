"""
Generated from SyncGroupRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/SyncGroupRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupRequestAssignment:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(14)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The ID of the member to assign."""
    assignment: bytes = field(metadata={"kafka_type": "bytes"})
    """The member assignment."""


@dataclass(frozen=True, slots=True, kw_only=True)
class SyncGroupRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(14)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
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
