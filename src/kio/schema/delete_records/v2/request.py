"""
Generated from DeleteRecordsRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/DeleteRecordsRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsPartition:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(21)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    offset: i64 = field(metadata={"kafka_type": "int64"})
    """The deletion offset."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsTopic:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(21)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[DeleteRecordsPartition, ...]
    """Each partition that we want to delete records from."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteRecordsRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(21)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topics: tuple[DeleteRecordsTopic, ...]
    """Each topic that we want to delete records from."""
    timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """How long to wait for the deletion to complete, in milliseconds."""
