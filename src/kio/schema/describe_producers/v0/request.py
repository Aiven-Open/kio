"""
Generated from DescribeProducersRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DescribeProducersRequest.json
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
class TopicRequest:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(61)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_indexes: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The indexes of the partitions to list producers for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeProducersRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(61)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[TopicRequest, ...]
