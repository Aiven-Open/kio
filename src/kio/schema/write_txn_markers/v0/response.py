"""
Generated from WriteTxnMarkersResponse.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/WriteTxnMarkersResponse.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.response_header.v0.header import ResponseHeader
from kio.schema.types import ProducerId
from kio.schema.types import TopicName
from kio.static.constants import ErrorCode
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarkerPartitionResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(27)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The error code, or 0 if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarkerTopicResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(27)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[WritableTxnMarkerPartitionResult, ...]
    """The results by partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class WritableTxnMarkerResult:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(27)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    """The current producer ID in use by the transactional ID."""
    topics: tuple[WritableTxnMarkerTopicResult, ...]
    """The results by topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class WriteTxnMarkersResponse(ApiMessage):
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(27)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    markers: tuple[WritableTxnMarkerResult, ...]
    """The results for writing makers."""
