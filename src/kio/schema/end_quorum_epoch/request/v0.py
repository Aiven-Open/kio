"""
Generated from EndQuorumEpochRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __flexible__: ClassVar[bool] = False
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The current leader ID that is resigning"""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current epoch"""
    preferred_successors: tuple[i32, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """A sorted list of preferred successors to start the election"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __flexible__: ClassVar[bool] = False
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class EndQuorumEpochRequest:
    __flexible__: ClassVar[bool] = False
    cluster_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    topics: tuple[TopicData, ...]
