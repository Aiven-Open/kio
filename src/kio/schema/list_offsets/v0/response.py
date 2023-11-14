"""
Generated from ListOffsetsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ListOffsetsResponse.json
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
class ListOffsetsPartitionResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition error code, or 0 if there was no error."""
    old_style_offsets: tuple[i64, ...] = field(
        metadata={"kafka_type": "int64"}, default=()
    )
    """The result offsets."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopicResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[ListOffsetsPartitionResponse, ...]
    """Each partition in the response."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topics: tuple[ListOffsetsTopicResponse, ...]
    """Each topic in the response."""
