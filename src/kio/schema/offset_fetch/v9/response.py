"""
Generated from ``clients/src/main/resources/common/message/OffsetFetchResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponsePartitions:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    committed_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The committed message offset."""
    committed_leader_epoch: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-1)
    )
    """The leader epoch."""
    metadata: str | None = field(metadata={"kafka_type": "string"})
    """The partition metadata."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition-level error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponseTopics:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetFetchResponsePartitions, ...]
    """The responses per partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponseGroup:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID."""
    topics: tuple[OffsetFetchResponseTopics, ...]
    """The responses per topic."""
    error_code: ErrorCode = field(
        metadata={"kafka_type": "error_code"}, default=ErrorCode(0)
    )
    """The group-level error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    groups: tuple[OffsetFetchResponseGroup, ...]
    """The responses per group id."""
