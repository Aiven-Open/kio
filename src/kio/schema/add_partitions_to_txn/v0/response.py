"""
Generated from AddPartitionsToTxnResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AddPartitionsToTxnResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnPartitionResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition indexes."""
    partition_error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The response error code."""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnTopicResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    results_by_partition: tuple[AddPartitionsToTxnPartitionResult, ...]
    """The results for each partition"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPartitionsToTxnResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(24)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """Duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    results_by_topic_v3_and_below: tuple[AddPartitionsToTxnTopicResult, ...]
    """The results for each topic."""
