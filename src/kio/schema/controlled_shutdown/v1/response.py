"""
Generated from ControlledShutdownResponse.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/ControlledShutdownResponse.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class RemainingPartition:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(7)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The index of the partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ControlledShutdownResponse:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(7)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The top-level error code."""
    remaining_partitions: tuple[RemainingPartition, ...]
    """The partitions that the broker still leads."""
