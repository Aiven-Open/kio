"""
Generated from ``clients/src/main/resources/common/message/FetchRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplicaState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(17)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"}, default=BrokerId(-1))
    """The replica ID of the follower, or -1 if this request is from a consumer."""
    replica_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The epoch of this follower, or -1 if not available."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchPartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(17)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    current_leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The current leader epoch of the partition."""
    fetch_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The message offset."""
    last_fetched_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The epoch of the last fetched record or -1 if there is none"""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The earliest available offset of the follower replica.  The field is only used when the request is sent by the follower."""
    partition_max_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum bytes to fetch from this partition.  See KIP-74 for cases where this limit may not be honored."""
    replica_directory_id: uuid.UUID | None = field(
        metadata={"kafka_type": "uuid", "tag": 0}, default=None
    )
    """The directory id of the follower fetching"""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(17)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID"""
    partitions: tuple[FetchPartition, ...]
    """The partitions to fetch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ForgottenTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(17)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID"""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions indexes to forget."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(17)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    cluster_id: str | None = field(
        metadata={"kafka_type": "string", "tag": 0}, default=None
    )
    """The clusterId if known. This is used to validate metadata fetches prior to broker registration."""
    replica_state: ReplicaState = field(metadata={"tag": 1}, default=ReplicaState())
    max_wait: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The maximum time in milliseconds to wait for the response."""
    min_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The minimum bytes to accumulate in the response."""
    max_bytes: i32 = field(metadata={"kafka_type": "int32"}, default=i32(2147483647))
    """The maximum bytes to fetch.  See KIP-74 for cases where this limit may not be honored."""
    isolation_level: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """This setting controls the visibility of transactional records. Using READ_UNCOMMITTED (isolation_level = 0) makes all records visible. With READ_COMMITTED (isolation_level = 1), non-transactional and COMMITTED transactional records are visible. To be more concrete, READ_COMMITTED returns all data from offsets smaller than the current LSO (last stable offset), and enables the inclusion of the list of aborted transactions in the result, which allows consumers to discard ABORTED transactional records"""
    session_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(0))
    """The fetch session ID."""
    session_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The fetch session epoch, which is used for ordering requests in a session."""
    topics: tuple[FetchTopic, ...]
    """The topics to fetch."""
    forgotten_topics_data: tuple[ForgottenTopic, ...]
    """In an incremental fetch request, the partitions to remove."""
    rack_id: str = field(metadata={"kafka_type": "string"}, default="")
    """Rack ID of the consumer making this request"""
