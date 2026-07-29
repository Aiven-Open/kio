"""
Generated from ``clients/src/main/resources/common/message/DescribeShareGroupOffsetsResponse.json``.
"""

import uuid

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
class DescribeShareGroupOffsetsResponsePartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(90)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    start_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The share-partition start offset."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The leader epoch of the partition."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition-level error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The partition-level error message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeShareGroupOffsetsResponseTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(90)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID."""
    partitions: tuple[DescribeShareGroupOffsetsResponsePartition, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeShareGroupOffsetsResponseGroup:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(90)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group identifier."""
    topics: tuple[DescribeShareGroupOffsetsResponseTopic, ...]
    """The results for each topic."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The group-level error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The group-level error message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeShareGroupOffsetsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(90)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    groups: tuple[DescribeShareGroupOffsetsResponseGroup, ...]
    """The results for each group."""
