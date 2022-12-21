"""
Generated from AlterPartitionRequest.json.
"""
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __flexible__: ClassVar[bool] = True
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index"""
    leader_epoch: int = field(metadata={"kafka_type": "int32"})
    """The leader epoch of this partition"""
    new_isr: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The ISR for this partition"""
    leader_recovery_state: int = field(metadata={"kafka_type": "int8"}, default=0)
    """1 if the partition is recovering from an unclean leader election; 0 otherwise."""
    partition_epoch: int = field(metadata={"kafka_type": "int32"})
    """The expected epoch of the partition which is being updated. For legacy cluster this is the ZkVersion in the LeaderAndIsr request."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __flexible__: ClassVar[bool] = True
    topic_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """The ID of the topic to alter ISRs for"""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterPartitionRequest:
    __flexible__: ClassVar[bool] = True
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the requesting broker"""
    broker_epoch: int = field(metadata={"kafka_type": "int64"}, default=-1)
    """The epoch of the requesting broker"""
    topics: tuple[TopicData, ...]
