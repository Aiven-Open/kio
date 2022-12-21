"""
Generated from StopReplicaRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaTopicV1:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_indexes: tuple[int, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The partition indexes."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaRequest:
    __flexible__: ClassVar[bool] = False
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The controller id."""
    controller_epoch: int = field(metadata={"kafka_type": "int32"})
    """The controller epoch."""
    broker_epoch: int = field(metadata={"kafka_type": "int64"}, default=-1)
    """The broker epoch."""
    delete_partitions: bool = field(metadata={"kafka_type": "bool"})
    """Whether these partitions should be deleted."""
    topics: tuple[StopReplicaTopicV1, ...]
    """The topics to stop."""
