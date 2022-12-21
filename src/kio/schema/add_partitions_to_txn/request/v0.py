"""
Generated from AddPartitionsToTxnRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TopicName
from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnTopic:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partitions: tuple[int, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partition indexes to add to the transaction"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnRequest:
    __flexible__: ClassVar[bool] = False
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The transactional id corresponding to the transaction."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """Current producer id in use by the transactional id."""
    producer_epoch: int = field(metadata={"kafka_type": "int16"})
    """Current epoch associated with the producer id."""
    topics: tuple[AddPartitionsToTxnTopic, ...]
    """The partitions to add to the transaction."""
