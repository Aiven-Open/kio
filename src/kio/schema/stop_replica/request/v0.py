"""
Generated from StopReplicaRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaPartitionV0:
    __flexible__: ClassVar[bool] = False
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaRequest:
    __flexible__: ClassVar[bool] = False
    controller_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The controller id."""
    controller_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The controller epoch."""
    delete_partitions: bool = field(metadata={"kafka_type": "bool"})
    """Whether these partitions should be deleted."""
    ungrouped_partitions: tuple[StopReplicaPartitionV0, ...]
    """The partitions to stop."""
