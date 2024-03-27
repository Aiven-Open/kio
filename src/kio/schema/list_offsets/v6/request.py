"""
Generated from ``clients/src/main/resources/common/message/ListOffsetsRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsPartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    current_leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The current leader epoch."""
    timestamp: i64 = field(metadata={"kafka_type": "int64"})
    """The current timestamp."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[ListOffsetsPartition, ...]
    """Each partition in the request."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(2)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the requester, or -1 if this request is being made by a normal consumer."""
    isolation_level: i8 = field(metadata={"kafka_type": "int8"})
    """This setting controls the visibility of transactional records. Using READ_UNCOMMITTED (isolation_level = 0) makes all records visible. With READ_COMMITTED (isolation_level = 1), non-transactional and COMMITTED transactional records are visible. To be more concrete, READ_COMMITTED returns all data from offsets smaller than the current LSO (last stable offset), and enables the inclusion of the list of aborted transactions in the result, which allows consumers to discard ABORTED transactional records"""
    topics: tuple[ListOffsetsTopic, ...]
    """Each topic in the request."""
