"""
Generated from DescribeQuorumResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplicaState:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    log_end_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The last known log end offset of the follower or -1 if it is unknown"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the current leader or -1 if the leader is unknown."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The latest known leader epoch"""
    high_watermark: i64 = field(metadata={"kafka_type": "int64"})
    current_voters: tuple[ReplicaState, ...]
    observers: tuple[ReplicaState, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeQuorumResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(55)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top level error code."""
    topics: tuple[TopicData, ...]
