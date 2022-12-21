"""
Generated from DescribeTransactionsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TopicName
from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __flexible__: ClassVar[bool] = True
    topic: TopicName = field(metadata={"kafka_type": "string"})
    partitions: tuple[int, ...] = field(metadata={"kafka_type": "int32"}, default=())


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionState:
    __flexible__: ClassVar[bool] = True
    error_code: int = field(metadata={"kafka_type": "int16"})
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    transaction_state: str = field(metadata={"kafka_type": "string"})
    transaction_timeout_ms: int = field(metadata={"kafka_type": "int32"})
    transaction_start_time_ms: int = field(metadata={"kafka_type": "int64"})
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    producer_epoch: int = field(metadata={"kafka_type": "int16"})
    topics: tuple[TopicData, ...]
    """The set of partitions included in the current transaction (if active). When a transaction is preparing to commit or abort, this will include only partitions which do not have markers."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTransactionsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    transaction_states: tuple[TransactionState, ...]
