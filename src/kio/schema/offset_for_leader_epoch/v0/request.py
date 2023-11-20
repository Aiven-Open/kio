"""
Generated from OffsetForLeaderEpochRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/OffsetForLeaderEpochRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderPartition:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch to look up an offset for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderTopic:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetForLeaderPartition, ...]
    """Each partition to get offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderEpochRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(23)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[OffsetForLeaderTopic, ...]
    """Each topic to get offsets for."""
