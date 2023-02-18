"""
Generated from FetchResponse.json.
"""
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import ProducerId
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class EpochEndOffset:
    __flexible__: ClassVar[bool] = True
    epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    end_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderIdAndEpoch:
    __flexible__: ClassVar[bool] = True
    leader_id: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(i32(-1))
    )
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The latest known leader epoch"""


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotId:
    __flexible__: ClassVar[bool] = True
    end_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))


@dataclass(frozen=True, slots=True, kw_only=True)
class AbortedTransaction:
    __flexible__: ClassVar[bool] = True
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The producer id associated with the aborted transaction."""
    first_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The first offset in the aborted transaction."""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no fetch error."""
    high_watermark: i64 = field(metadata={"kafka_type": "int64"})
    """The current high water mark."""
    last_stable_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The last stable offset (or LSO) of the partition. This is the last offset such that the state of all transactional records prior to this offset have been decided (ABORTED or COMMITTED)"""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The current log start offset."""
    diverging_epoch: EpochEndOffset
    """In case divergence is detected based on the `LastFetchedEpoch` and `FetchOffset` in the request, this field indicates the largest epoch and its end offset such that subsequent records are known to diverge"""
    current_leader: LeaderIdAndEpoch
    snapshot_id: SnapshotId
    """In the case of fetching an offset less than the LogStartOffset, this is the end offset and epoch that should be used in the FetchSnapshot request."""
    aborted_transactions: tuple[AbortedTransaction, ...]
    """The aborted transactions."""
    preferred_read_replica: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(i32(-1))
    )
    """The preferred read replica for the consumer to use on its next fetch request"""
    records: tuple[bytes | None, ...] | None = field(metadata={"kafka_type": "records"})
    """The record data."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchableTopicResponse:
    __flexible__: ClassVar[bool] = True
    topic_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID"""
    partitions: tuple[PartitionData, ...]
    """The topic partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top level response error code."""
    session_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(0))
    """The fetch session ID, or 0 if this is not part of a fetch session."""
    responses: tuple[FetchableTopicResponse, ...]
    """The response topics."""
