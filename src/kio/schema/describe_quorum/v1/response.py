"""
Generated from ``clients/src/main/resources/common/message/DescribeQuorumResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplicaState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    log_end_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The last known log end offset of the follower or -1 if it is unknown"""
    last_fetch_timestamp: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The last known leader wall clock time time when a follower fetched from the leader. This is reported as -1 both for the current leader or if it is unknown for a voter"""
    last_caught_up_timestamp: i64 = field(
        metadata={"kafka_type": "int64"}, default=i64(-1)
    )
    """The leader wall clock append time of the offset for which the follower made the most recent fetch request. This is reported as the current time for the leader and -1 if unknown for a voter"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The latest known leader epoch"""
    high_watermark: i64 = field(metadata={"kafka_type": "int64"})
    current_voters: tuple[ReplicaState, ...]
    observers: tuple[ReplicaState, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeQuorumResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top level error code."""
    topics: tuple[TopicData, ...]
