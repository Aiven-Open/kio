"""
Generated from DescribeLogDirsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeLogDirsRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribableLogDirTopic:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(35)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partition indexes."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeLogDirsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(35)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[DescribableLogDirTopic, ...]
    """Each topic that we want to describe log directories for, or null for all topics."""
