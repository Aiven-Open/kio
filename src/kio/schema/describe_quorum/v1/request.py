"""
Generated from DescribeQuorumRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeQuorumRequest.json
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
class PartitionData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeQuorumRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[TopicData, ...]
