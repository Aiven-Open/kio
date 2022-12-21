"""
Generated from ListTransactionsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionState:
    __flexible__: ClassVar[bool] = True
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    transaction_state: str = field(metadata={"kafka_type": "string"})
    """The current transaction state of the producer"""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListTransactionsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    unknown_state_filters: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """Set of state filters provided in the request which were unknown to the transaction coordinator"""
    transaction_states: tuple[TransactionState, ...]
