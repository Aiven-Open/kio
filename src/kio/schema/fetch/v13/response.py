"""
Generated from ``clients/src/main/resources/common/message/FetchResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.schema.types import ProducerId
from kio.static.constants import EntityType
from kio.static.primitive import Records
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class EpochEndOffset:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(13)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    end_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderIdAndEpoch:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(13)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"}, default=BrokerId(-1))
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The latest known leader epoch"""


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotId:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(13)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    end_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))


@dataclass(frozen=True, slots=True, kw_only=True)
class AbortedTransaction:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(13)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The producer id associated with the aborted transaction."""
    first_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The first offset in the aborted transaction."""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(13)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no fetch error."""
    high_watermark: i64 = field(metadata={"kafka_type": "int64"})
    """The current high water mark."""
    last_stable_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The last stable offset (or LSO) of the partition. This is the last offset such that the state of all transactional records prior to this offset have been decided (ABORTED or COMMITTED)"""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The current log start offset."""
    diverging_epoch: EpochEndOffset = field(
        metadata={"tag": 0}, default=EpochEndOffset()
    )
    """In case divergence is detected based on the `LastFetchedEpoch` and `FetchOffset` in the request, this field indicates the largest epoch and its end offset such that subsequent records are known to diverge"""
    current_leader: LeaderIdAndEpoch = field(
        metadata={"tag": 1}, default=LeaderIdAndEpoch()
    )
    snapshot_id: SnapshotId = field(metadata={"tag": 2}, default=SnapshotId())
    """In the case of fetching an offset less than the LogStartOffset, this is the end offset and epoch that should be used in the FetchSnapshot request."""
    aborted_transactions: tuple[AbortedTransaction, ...] | None
    """The aborted transactions."""
    preferred_read_replica: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(-1)
    )
    """The preferred read replica for the consumer to use on its next fetch request"""
    records: Records | None = field(metadata={"kafka_type": "records"})
    """The record data."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchableTopicResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(13)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID"""
    partitions: tuple[PartitionData, ...]
    """The topic partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(13)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top level response error code."""
    session_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(0))
    """The fetch session ID, or 0 if this is not part of a fetch session."""
    responses: tuple[FetchableTopicResponse, ...]
    """The response topics."""
