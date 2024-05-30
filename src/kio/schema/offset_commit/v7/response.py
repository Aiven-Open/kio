"""
Generated from ``clients/src/main/resources/common/message/OffsetCommitResponse.json``.
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
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitResponsePartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(8)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitResponseTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(8)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetCommitResponsePartition, ...]
    """The responses for each partition in the topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(8)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[OffsetCommitResponseTopic, ...]
    """The responses for each topic."""
