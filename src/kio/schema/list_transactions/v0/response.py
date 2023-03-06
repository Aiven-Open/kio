"""
Generated from ListTransactionsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.schema.types import TransactionalId


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionState:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(66)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    transaction_state: str = field(metadata={"kafka_type": "string"})
    """The current transaction state of the producer"""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListTransactionsResponse:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(66)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    unknown_state_filters: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """Set of state filters provided in the request which were unknown to the transaction coordinator"""
    transaction_states: tuple[TransactionState, ...]
