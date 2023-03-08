"""
Generated from OffsetFetchResponse.json.
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
class OffsetFetchResponsePartition:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = False
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
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponseTopic:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetFetchResponsePartition, ...]
    """The responses per partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponse:
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[OffsetFetchResponseTopic, ...]
    """The responses per topic."""
    error_code: i16 = field(metadata={"kafka_type": "int16"}, default=i16(0))
    """The top-level error code, or 0 if there was no error."""
