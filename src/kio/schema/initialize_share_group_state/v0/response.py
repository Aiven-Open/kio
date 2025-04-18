"""
Generated from ``clients/src/main/resources/common/message/InitializeShareGroupStateResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(83)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The error message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class InitializeStateResult:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(83)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The topic identifier"""
    partitions: tuple[PartitionResult, ...]
    """The results for the partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class InitializeShareGroupStateResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(83)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    results: tuple[InitializeStateResult, ...]
    """The initialization results"""
