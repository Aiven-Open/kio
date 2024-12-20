"""
Generated from ``clients/src/main/resources/common/message/AddPartitionsToTxnResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import TopicName
from kio.schema.types import TransactionalId
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnPartitionResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition indexes."""
    partition_error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The response error code."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnTopicResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    results_by_partition: tuple[AddPartitionsToTxnPartitionResult, ...]
    """The results for each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    transactional_id: TransactionalId = field(metadata={"kafka_type": "string"})
    """The transactional id corresponding to the transaction."""
    topic_results: tuple[AddPartitionsToTxnTopicResult, ...]
    """The results for each topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(5)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The response top level error code."""
    results_by_transaction: tuple[AddPartitionsToTxnResult, ...]
    """Results categorized by transactional ID."""
