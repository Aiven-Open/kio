"""
Generated from ``clients/src/main/resources/common/message/FetchResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import Records
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class AbortedTransaction:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The producer id associated with the aborted transaction."""
    first_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The first offset in the aborted transaction."""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no fetch error."""
    high_watermark: i64 = field(metadata={"kafka_type": "int64"})
    """The current high water mark."""
    last_stable_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The last stable offset (or LSO) of the partition. This is the last offset such that the state of all transactional records prior to this offset have been decided (ABORTED or COMMITTED)"""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The current log start offset."""
    aborted_transactions: tuple[AbortedTransaction, ...] | None
    """The aborted transactions."""
    records: Records | None = field(metadata={"kafka_type": "records"})
    """The record data."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchableTopicResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[PartitionData, ...]
    """The topic partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top level response error code."""
    session_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(0))
    """The fetch session ID, or 0 if this is not part of a fetch session."""
    responses: tuple[FetchableTopicResponse, ...]
    """The response topics."""
