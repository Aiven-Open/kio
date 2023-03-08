"""
Generated from StopReplicaResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaPartitionError:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(5)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The partition error code, or 0 if there was no partition error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaResponse:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(5)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top-level error code, or 0 if there was no top-level error."""
    partition_errors: tuple[StopReplicaPartitionError, ...]
    """The responses for each partition."""
