"""
Generated from ProduceResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ProduceResponse.json
"""

import datetime
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import TZAware
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.primitive import i64
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class BatchIndexAndErrorMessage:
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
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
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""
    base_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The base offset."""
    log_append_time: TZAware | None = field(
        metadata={"kafka_type": "datetime_i64"}, default=None
    )
    """The timestamp returned by broker after appending the messages. If CreateTime is used for the topic, the timestamp will be -1.  If LogAppendTime is used for the topic, the timestamp will be the broker local time when the messages are appended."""
    log_start_offset: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The log start offset."""
    record_errors: tuple[BatchIndexAndErrorMessage, ...]
    """The batch indices of records that caused the batch to be dropped"""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The global error message summarizing the common root cause of the records that caused the batch to be dropped"""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicProduceResponse:
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partition_responses: tuple[PartitionProduceResponse, ...]
    """Each partition that we produced to within the topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ProduceResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(8)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(0)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    responses: tuple[TopicProduceResponse, ...]
    """Each produce response"""
    throttle_time: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=0)),
    )
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
