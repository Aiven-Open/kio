"""
Generated from LeaderAndIsrRequest.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/LeaderAndIsrRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrPartitionState:
    __version__: ClassVar[i16] = i16(4)
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


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrTopicState:
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_states: tuple[LeaderAndIsrPartitionState, ...]
    """The state of each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrLiveLeader:
    __version__: ClassVar[i16] = i16(4)
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
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The current controller ID."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current controller epoch."""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The current broker epoch."""
    topic_states: tuple[LeaderAndIsrTopicState, ...]
    """Each topic."""
    live_leaders: tuple[LeaderAndIsrLiveLeader, ...]
    """The current live leaders."""
