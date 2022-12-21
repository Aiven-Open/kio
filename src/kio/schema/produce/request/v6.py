"""
Generated from ProduceRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionProduceData:
    __flexible__: ClassVar[bool] = False
    index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    records: tuple[bytes | None, ...] | None = field(metadata={"kafka_type": "records"})
    """The record data to be produced."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicProduceData:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_data: tuple[PartitionProduceData, ...]
    """Each partition to produce to."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ProduceRequest:
    __flexible__: ClassVar[bool] = False
    transactional_id: TransactionalId | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The transactional ID, or null if the producer is not transactional."""
    acks: int = field(metadata={"kafka_type": "int16"})
    """The number of acknowledgments the producer requires the leader to have received before considering a request complete. Allowed values: 0 for no acknowledgments, 1 for only the leader and -1 for the full ISR."""
    timeout_ms: int = field(metadata={"kafka_type": "int32"})
    """The timeout to await a response in milliseconds."""
    topic_data: tuple[TopicProduceData, ...]
    """Each topic to produce to."""
