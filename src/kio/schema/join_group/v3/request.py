"""
Generated from ``clients/src/main/resources/common/message/JoinGroupRequest.json``.
"""

import datetime

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import GroupId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupRequestProtocol:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(11)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The protocol name."""
    metadata: bytes = field(metadata={"kafka_type": "bytes"})
    """The protocol metadata."""


@dataclass(frozen=True, slots=True, kw_only=True)
class JoinGroupRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(11)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group identifier."""
    session_timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The coordinator considers the consumer dead if it receives no heartbeat after this timeout in milliseconds."""
    rebalance_timeout: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=-1)),
    )
    """The maximum time in milliseconds that the coordinator will wait for each member to rejoin when rebalancing the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member id assigned by the group coordinator."""
    protocol_type: str = field(metadata={"kafka_type": "string"})
    """The unique name the for class of protocols implemented by the group we want to join."""
    protocols: tuple[JoinGroupRequestProtocol, ...]
    """The list of protocols that the member supports."""
