"""
Generated from FetchSnapshotRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotId:
    __flexible__: ClassVar[bool] = True
    end_offset: int = field(metadata={"kafka_type": "int64"})
    epoch: int = field(metadata={"kafka_type": "int32"})


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionSnapshot:
    __flexible__: ClassVar[bool] = True
    partition: int = field(metadata={"kafka_type": "int32"})
    """The partition index"""
    current_leader_epoch: int = field(metadata={"kafka_type": "int32"})
    """The current leader epoch of the partition, -1 for unknown leader epoch"""
    snapshot_id: SnapshotId
    """The snapshot endOffset and epoch to fetch"""
    position: int = field(metadata={"kafka_type": "int64"})
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
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"}, default=BrokerId(-1))
    """The broker ID of the follower"""
    max_bytes: int = field(metadata={"kafka_type": "int32"}, default=2147483647)
    """The maximum bytes to fetch from all of the snapshots"""
    topics: tuple[TopicSnapshot, ...]
    """The topics to fetch"""
