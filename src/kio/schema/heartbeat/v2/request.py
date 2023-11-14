"""
Generated from HeartbeatRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/HeartbeatRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class HeartbeatRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(12)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group id."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"})
    """The generation of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID."""
