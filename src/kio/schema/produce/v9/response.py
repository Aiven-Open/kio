"""
Generated from ProduceResponse.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class BatchIndexAndErrorMessage:
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    batch_index: i32 = field(metadata={"kafka_type": "int32"})
    """The batch index of the record that cause the batch to be dropped"""
    batch_index_error_message: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """The error message of the record that caused the batch to be dropped"""


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionProduceResponse:
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The error code, or 0 if there was no error."""
    base_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The base offset."""
    log_append_time_ms: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The timestamp returned by broker after appending the messages. If CreateTime is used for the topic, the timestamp will be -1.  If LogAppendTime is used for the topic, the timestamp will be the broker local time when the messages are appended."""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The log start offset."""
    record_errors: tuple[BatchIndexAndErrorMessage, ...]
    """The batch indices of records that caused the batch to be dropped"""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The global error message summarizing the common root cause of the records that caused the batch to be dropped"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicProduceResponse:
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partition_responses: tuple[PartitionProduceResponse, ...]
    """Each partition that we produced to within the topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ProduceResponse:
    __version__: ClassVar[i16] = i16(9)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    responses: tuple[TopicProduceResponse, ...]
    """Each produce response"""
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"}, default=i32(0))
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
