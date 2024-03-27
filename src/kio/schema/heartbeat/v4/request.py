"""
Generated from ``clients/src/main/resources/common/message/HeartbeatRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class HeartbeatRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(12)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group id."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The generation of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The unique identifier of the consumer instance provided by end user."""
