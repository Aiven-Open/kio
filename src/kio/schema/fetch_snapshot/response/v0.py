"""
Generated from FetchSnapshotResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotId:
    __flexible__: ClassVar[bool] = True
    end_offset: i64 = field(metadata={"kafka_type": "int64"})
    epoch: i32 = field(metadata={"kafka_type": "int32"})


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderIdAndEpoch:
    __flexible__: ClassVar[bool] = True
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The latest known leader epoch"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionSnapshot:
    __flexible__: ClassVar[bool] = True
    index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no fetch error."""
    snapshot_id: SnapshotId
    """The snapshot endOffset and epoch fetched"""
    current_leader: LeaderIdAndEpoch
    size: i64 = field(metadata={"kafka_type": "int64"})
    """The total size of the snapshot."""
    position: i64 = field(metadata={"kafka_type": "int64"})
    """The starting byte position within the snapshot included in the Bytes field."""
    unaligned_records: tuple[bytes | None, ...] = field(
        metadata={"kafka_type": "records"}
    )
    """Snapshot data in records format which may not be aligned on an offset boundary"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicSnapshot:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to fetch."""
    partitions: tuple[PartitionSnapshot, ...]
    """The partitions to fetch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchSnapshotResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top level response error code."""
    topics: tuple[TopicSnapshot, ...]
    """The topics to fetch."""
