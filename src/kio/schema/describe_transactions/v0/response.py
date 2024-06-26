"""
Generated from ``clients/src/main/resources/common/message/DescribeTransactionsResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.schema.types import TransactionalId
from kio.static.constants import EntityType
from kio.static.primitive import TZAware
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(65)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())


@dataclass(frozen=True, slots=True, kw_only=True)
class TransactionState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(65)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    transaction_state: str = field(metadata={"kafka_type": "string"})
    transaction_timeout: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    transaction_start_time: TZAware = field(metadata={"kafka_type": "datetime_i64"})
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    producer_epoch: i16 = field(metadata={"kafka_type": "int16"})
    topics: tuple[TopicData, ...]
    """The set of partitions included in the current transaction (if active). When a transaction is preparing to commit or abort, this will include only partitions which do not have markers."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTransactionsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(65)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    transaction_states: tuple[TransactionState, ...]
