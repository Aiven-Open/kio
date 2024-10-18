"""
Generated from ``clients/src/main/resources/common/message/DescribeTopicPartitionsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicRequest:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(75)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""


@dataclass(frozen=True, slots=True, kw_only=True)
class Cursor:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(75)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The name for the first topic to process"""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index to start with"""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTopicPartitionsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(75)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[TopicRequest, ...]
    """The topics to fetch details for."""
    response_partition_limit: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(2000)
    )
    """The maximum number of partitions included in the response."""
    cursor: Cursor | None = field(default=None)
    """The first topic and partition index to fetch details for."""
