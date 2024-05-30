"""
Generated from ``clients/src/main/resources/common/message/FetchSnapshotResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import Records
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class SnapshotId:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    end_offset: i64 = field(metadata={"kafka_type": "int64"})
    epoch: i32 = field(metadata={"kafka_type": "int32"})


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderIdAndEpoch:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The latest known leader epoch"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionSnapshot:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no fetch error."""
    snapshot_id: SnapshotId
    """The snapshot endOffset and epoch fetched"""
    current_leader: LeaderIdAndEpoch = field(metadata={"tag": 0})
    size: i64 = field(metadata={"kafka_type": "int64"})
    """The total size of the snapshot."""
    position: i64 = field(metadata={"kafka_type": "int64"})
    """The starting byte position within the snapshot included in the Bytes field."""
    unaligned_records: Records = field(metadata={"kafka_type": "records"})
    """Snapshot data in records format which may not be aligned on an offset boundary"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicSnapshot:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to fetch."""
    partitions: tuple[PartitionSnapshot, ...]
    """The partitions to fetch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchSnapshotResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(59)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top level response error code."""
    topics: tuple[TopicSnapshot, ...]
    """The topics to fetch."""
