"""
Generated from VoteRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import BrokerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    candidate_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The bumped epoch of the candidate sending the request"""
    candidate_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the voter sending the request"""
    last_offset_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The epoch of the last record written to the metadata log"""
    last_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The offset of the last record written to the metadata log"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __flexible__: ClassVar[bool] = True
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class VoteRequest:
    __flexible__: ClassVar[bool] = True
    cluster_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    topics: tuple[TopicData, ...]
