"""
Generated from OffsetForLeaderEpochRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderPartition:
    __flexible__: ClassVar[bool] = False
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    current_leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """An epoch used to fence consumers/replicas with old metadata. If the epoch provided by the client is larger than the current epoch known to the broker, then the UNKNOWN_LEADER_EPOCH error code will be returned. If the provided epoch is smaller, then the FENCED_LEADER_EPOCH error code will be returned."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch to look up an offset for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderTopic:
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetForLeaderPartition, ...]
    """Each partition to get offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderEpochRequest:
    __flexible__: ClassVar[bool] = False
    replica_id: BrokerId = field(
        metadata={"kafka_type": "int32"}, default=BrokerId(i32(-2))
    )
    """The broker ID of the follower, of -1 if this request is from a consumer."""
    topics: tuple[OffsetForLeaderTopic, ...]
    """Each topic to get offsets for."""
