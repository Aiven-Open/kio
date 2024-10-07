"""
Generated from ``clients/src/main/resources/common/message/ReadShareGroupStateResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class StateBatch:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(84)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    first_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The base offset of this state batch."""
    last_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The last offset of this state batch."""
    delivery_state: i8 = field(metadata={"kafka_type": "int8"})
    """The state - 0:Available,2:Acked,4:Archived."""
    delivery_count: i16 = field(metadata={"kafka_type": "int16"})
    """The delivery count."""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(84)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The error message, or null if there was no error."""
    state_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The state epoch for this share-partition."""
    start_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The share-partition start offset, which can be -1 if it is not yet initialized."""
    state_batches: tuple[StateBatch, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadStateResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(84)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The topic identifier"""
    partitions: tuple[PartitionResult, ...]
    """The results for the partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadShareGroupStateResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(84)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    results: tuple[ReadStateResult, ...]
    """The read results"""
