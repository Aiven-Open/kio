"""
Generated from LeaderAndIsrRequest.json.
"""
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i8
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrPartitionState:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The controller epoch."""
    leader: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the leader."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The leader epoch."""
    isr: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The in-sync replica IDs."""
    partition_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current epoch for the partition. The epoch is a monotonically increasing value which is incremented after every partition change. (Since the LeaderAndIsr request is only used by the legacy controller, this corresponds to the zkVersion)"""
    replicas: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The replica IDs."""
    adding_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The replica IDs that we are adding this partition to, or null if no replicas are being added."""
    removing_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The replica IDs that we are removing this partition from, or null if no replicas are being removed."""
    is_new: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """Whether the replica should have existed on the broker or not."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrTopicState:
    __flexible__: ClassVar[bool] = True
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    topic_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID."""
    partition_states: tuple[LeaderAndIsrPartitionState, ...]
    """The state of each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrLiveLeader:
    __flexible__: ClassVar[bool] = True
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The leader's broker ID."""
    host_name: str = field(metadata={"kafka_type": "string"})
    """The leader's hostname."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The leader's port."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrRequest:
    __flexible__: ClassVar[bool] = True
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The current controller ID."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current controller epoch."""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The current broker epoch."""
    type: i8 = field(metadata={"kafka_type": "int8"})
    """The type that indicates whether all topics are included in the request"""
    topic_states: tuple[LeaderAndIsrTopicState, ...]
    """Each topic."""
    live_leaders: tuple[LeaderAndIsrLiveLeader, ...]
    """The current live leaders."""
