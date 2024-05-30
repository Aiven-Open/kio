"""
Generated from ``clients/src/main/resources/common/message/StopReplicaResponse.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaPartitionError:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(5)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition error code, or 0 if there was no partition error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(4)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(5)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error code, or 0 if there was no top-level error."""
    partition_errors: tuple[StopReplicaPartitionError, ...]
    """The responses for each partition."""
