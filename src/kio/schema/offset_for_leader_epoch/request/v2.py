"""
Generated from OffsetForLeaderEpochRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetForLeaderPartition:
    __flexible__: ClassVar[bool] = False
    partition: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    current_leader_epoch: int = field(metadata={"kafka_type": "int32"}, default=-1)
    """An epoch used to fence consumers/replicas with old metadata. If the epoch provided by the client is larger than the current epoch known to the broker, then the UNKNOWN_LEADER_EPOCH error code will be returned. If the provided epoch is smaller, then the FENCED_LEADER_EPOCH error code will be returned."""
    leader_epoch: int = field(metadata={"kafka_type": "int32"})
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
    topics: tuple[OffsetForLeaderTopic, ...]
    """Each topic to get offsets for."""
