"""
Generated from ``clients/src/main/resources/common/message/FetchSnapshotRequest.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotId:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    end_offset: i64 = field(metadata={"kafka_type": "int64"})
    epoch: i32 = field(metadata={"kafka_type": "int32"})


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionSnapshot:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
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
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to fetch"""
    partitions: tuple[PartitionSnapshot, ...]
    """The partitions to fetch"""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchSnapshotRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    cluster_id: str | None = field(
        metadata={"kafka_type": "string", "tag": 0}, default=None
    )
    """The clusterId if known, this is used to validate metadata fetches prior to broker registration"""
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"}, default=BrokerId(-1))
    """The broker ID of the follower"""
    max_bytes: i32 = field(metadata={"kafka_type": "int32"}, default=i32(2147483647))
    """The maximum bytes to fetch from all of the snapshots"""
    topics: tuple[TopicSnapshot, ...]
    """The topics to fetch"""
