"""
Generated from ``clients/src/main/resources/common/message/DescribeProducersResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ProducerState:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(61)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    producer_epoch: i32 = field(metadata={"kafka_type": "int32"})
    last_sequence: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    last_timestamp: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    coordinator_epoch: i32 = field(metadata={"kafka_type": "int32"})
    current_txn_start_offset: i64 = field(
        metadata={"kafka_type": "int64"}, default=i64(-1)
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(61)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The partition error message, which may be null if no additional details are available"""
    active_producers: tuple[ProducerState, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicResponse:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(61)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[PartitionResponse, ...]
    """Each partition in the response."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeProducersResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(61)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[TopicResponse, ...]
    """Each topic in the response."""
