"""
Generated from OffsetForLeaderEpochResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class EpochEndOffset:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code 0, or if there was no error."""
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    end_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The end offset of the epoch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderTopicResult:
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
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topics: tuple[OffsetForLeaderTopicResult, ...]
    """Each topic we fetched offsets for."""
