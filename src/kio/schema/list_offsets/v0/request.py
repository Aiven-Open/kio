"""
Generated from ``clients/src/main/resources/common/message/ListOffsetsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsPartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    timestamp: i64 = field(metadata={"kafka_type": "int64"})
    """The current timestamp."""
    max_num_offsets: i32 = field(metadata={"kafka_type": "int32"}, default=i32(1))
    """The maximum number of offsets to report."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[ListOffsetsPartition, ...]
    """Each partition in the request."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the requester, or -1 if this request is being made by a normal consumer."""
    topics: tuple[ListOffsetsTopic, ...]
    """Each topic in the request."""
