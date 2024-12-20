"""
Generated from ``clients/src/main/resources/common/message/ShareGroupHeartbeatResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartitions:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(76)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The topic ID."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Assignment:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(76)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_partitions: tuple[TopicPartitions, ...]
    """The partitions assigned to the member."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ShareGroupHeartbeatResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(76)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error code, or 0 if there was no error"""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The top-level error message, or null if there was no error."""
    member_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The member ID generated by the coordinator. Only provided when the member joins with MemberEpoch == 0."""
    member_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The member epoch."""
    heartbeat_interval: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The heartbeat interval in milliseconds."""
    assignment: Assignment | None = field(default=None)
    """null if not provided; the assignment otherwise."""
