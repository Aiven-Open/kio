"""
Generated from OffsetCommitRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId
from kio.schema.entity import TopicName
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitRequestPartition:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    committed_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The message offset to be committed."""
    committed_leader_epoch: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-1)
    )
    """The leader epoch of this partition."""
    committed_metadata: str | None = field(metadata={"kafka_type": "string"})
    """Any associated metadata the client wants to keep."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitRequestTopic:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[OffsetCommitRequestPartition, ...]
    """Each partition to commit offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class OffsetCommitRequest:
    __flexible__: ClassVar[bool] = True
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The unique group identifier."""
    generation_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The generation of the group."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID assigned by the group coordinator."""
    group_instance_id: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The unique identifier of the consumer instance provided by end user."""
    topics: tuple[OffsetCommitRequestTopic, ...]
    """The topics to commit offsets for."""
