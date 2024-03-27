"""
Generated from ``clients/src/main/resources/common/message/FetchRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchPartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    fetch_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The message offset."""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The earliest available offset of the follower replica.  The field is only used when the request is sent by the follower."""
    partition_max_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum bytes to fetch from this partition.  See KIP-74 for cases where this limit may not be honored."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to fetch."""
    partitions: tuple[FetchPartition, ...]
    """The partitions to fetch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"}, default=BrokerId(-1))
    """The broker ID of the follower, of -1 if this request is from a consumer."""
    max_wait: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The maximum time in milliseconds to wait for the response."""
    min_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The minimum bytes to accumulate in the response."""
    max_bytes: i32 = field(metadata={"kafka_type": "int32"}, default=i32(2147483647))
    """The maximum bytes to fetch.  See KIP-74 for cases where this limit may not be honored."""
    isolation_level: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """This setting controls the visibility of transactional records. Using READ_UNCOMMITTED (isolation_level = 0) makes all records visible. With READ_COMMITTED (isolation_level = 1), non-transactional and COMMITTED transactional records are visible. To be more concrete, READ_COMMITTED returns all data from offsets smaller than the current LSO (last stable offset), and enables the inclusion of the list of aborted transactions in the result, which allows consumers to discard ABORTED transactional records"""
    topics: tuple[FetchTopic, ...]
    """The topics to fetch."""
