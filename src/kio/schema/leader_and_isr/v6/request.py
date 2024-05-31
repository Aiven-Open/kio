"""
Generated from ``clients/src/main/resources/common/message/LeaderAndIsrRequest.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrPartitionState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
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
    leader_recovery_state: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """1 if the partition is recovering from an unclean leader election; 0 otherwise."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrTopicState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID."""
    partition_states: tuple[LeaderAndIsrPartitionState, ...]
    """The state of each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrLiveLeader:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The leader's broker ID."""
    host_name: str = field(metadata={"kafka_type": "string"})
    """The leader's hostname."""
    port: i32 = field(metadata={"kafka_type": "int32"})
    """The leader's port."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrRequest:
    __type__: ClassVar = EntityType.request
    __version__: ClassVar[i16] = i16(6)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The current controller ID."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current controller epoch."""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The current broker epoch."""
    type_: i8 = field(metadata={"kafka_type": "int8"})
    """The type that indicates whether all topics are included in the request"""
    topic_states: tuple[LeaderAndIsrTopicState, ...]
    """Each topic."""
    live_leaders: tuple[LeaderAndIsrLiveLeader, ...]
    """The current live leaders."""
