"""
Generated from LeaderAndIsrResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/LeaderAndIsrResponse.json
"""

import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v1.header import ResponseHeader
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrPartitionError:
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrTopicError:
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID"""
    partition_errors: tuple[LeaderAndIsrPartitionError, ...]
    """Each partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LeaderAndIsrResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(7)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(4)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    topics: tuple[LeaderAndIsrTopicError, ...]
    """Each topic"""
