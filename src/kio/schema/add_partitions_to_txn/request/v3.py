"""
Generated from AddPartitionsToTxnRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TopicName
from kio.schema.entity import TransactionalId
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnTopic:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partition indexes to add to the transaction"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnRequest:
    __flexible__: ClassVar[bool] = True
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The transactional id corresponding to the transaction."""
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """Current producer id in use by the transactional id."""
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    """Current epoch associated with the producer id."""
    topics: tuple[AddPartitionsToTxnTopic, ...]
    """The partitions to add to the transaction."""
