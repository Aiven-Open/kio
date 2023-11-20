"""
Generated from OffsetFetchResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/OffsetFetchResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponsePartition:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    committed_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The committed message offset."""
    metadata: str | None = field(metadata={"kafka_type": "string"})
    """The partition metadata."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponseTopic:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetFetchResponsePartition, ...]
    """The responses per partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetFetchResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(9)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topics: tuple[OffsetFetchResponseTopic, ...]
    """The responses per topic."""
    error_code: ErrorCode = field(
        metadata={"kafka_type": "error_code"}, default=ErrorCode(0)
    )
    """The top-level error code, or 0 if there was no error."""
