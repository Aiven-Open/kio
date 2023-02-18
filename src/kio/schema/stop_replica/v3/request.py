"""
Generated from StopReplicaRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaPartitionState:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The leader epoch."""
    delete_partition: bool = field(metadata={"kafka_type": "bool"})
    """Whether this partition should be deleted."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaTopicState:
    __flexible__: ClassVar[bool] = True
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_states: tuple[StopReplicaPartitionState, ...]
    """The state of each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaRequest:
    __flexible__: ClassVar[bool] = True
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The controller id."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The controller epoch."""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The broker epoch."""
    topic_states: tuple[StopReplicaTopicState, ...]
    """Each topic."""
