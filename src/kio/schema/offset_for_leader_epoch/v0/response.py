"""
Generated from ``clients/src/main/resources/common/message/OffsetForLeaderEpochResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class EpochEndOffset:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code 0, or if there was no error."""
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    end_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The end offset of the epoch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderTopicResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[EpochEndOffset, ...]
    """Each partition in the topic we fetched offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderEpochResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topics: tuple[OffsetForLeaderTopicResult, ...]
    """Each topic we fetched offsets for."""
