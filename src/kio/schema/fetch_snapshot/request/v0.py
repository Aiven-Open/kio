"""
Generated from FetchSnapshotRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotId:
    __flexible__: ClassVar[bool] = True
    end_offset: i64 = field(metadata={"kafka_type": "int64"})
    epoch: i32 = field(metadata={"kafka_type": "int32"})


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionSnapshot:
    __flexible__: ClassVar[bool] = True
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index"""
    current_leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current leader epoch of the partition, -1 for unknown leader epoch"""
    snapshot_id: SnapshotId
    """The snapshot endOffset and epoch to fetch"""
    position: i64 = field(metadata={"kafka_type": "int64"})
    """The byte position within the snapshot to start fetching from"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicSnapshot:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to fetch"""
    partitions: tuple[PartitionSnapshot, ...]
    """The partitions to fetch"""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchSnapshotRequest:
    __flexible__: ClassVar[bool] = True
    cluster_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The clusterId if known, this is used to validate metadata fetches prior to broker registration"""
    replica_id: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(i32(-1))
    )
    """The broker ID of the follower"""
    max_bytes: i32 = field(metadata={"kafka_type": "int32"}, default=i32(2147483647))
    """The maximum bytes to fetch from all of the snapshots"""
    topics: tuple[TopicSnapshot, ...]
    """The topics to fetch"""
