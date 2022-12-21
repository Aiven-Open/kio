"""
Generated from TxnOffsetCommitRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import GroupId
from kio.schema.entity import ProducerId
from kio.schema.entity import TopicName
from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class TxnOffsetCommitRequestPartition:
    __flexible__: ClassVar[bool] = False
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The index of the partition within the topic."""
    committed_offset: int = field(metadata={"kafka_type": "int64"})
    """The message offset to be committed."""
    committed_leader_epoch: int = field(metadata={"kafka_type": "int32"}, default=-1)
    """The leader epoch of the last consumed record."""
    committed_metadata: str | None = field(metadata={"kafka_type": "string"})
    """Any associated metadata the client wants to keep."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TxnOffsetCommitRequestTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[TxnOffsetCommitRequestPartition, ...]
    """The partitions inside the topic that we want to committ offsets for."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TxnOffsetCommitRequest:
    __flexible__: ClassVar[bool] = False
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The ID of the transaction."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The ID of the group."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The current producer ID in use by the transactional ID."""
    producer_epoch: int = field(metadata={"kafka_type": "int16"})
    """The current epoch associated with the producer ID."""
    topics: tuple[TxnOffsetCommitRequestTopic, ...]
    """Each topic that we want to commit offsets for."""
