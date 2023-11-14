"""
Generated from ListTransactionsResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ListTransactionsResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.schema.types import TransactionalId
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


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
class ListTransactionsResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(66)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    unknown_state_filters: tuple[str, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """Set of state filters provided in the request which were unknown to the transaction coordinator"""
    transaction_states: tuple[TransactionState, ...]
