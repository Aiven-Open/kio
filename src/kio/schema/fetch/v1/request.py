"""
Generated from FetchRequest.json.
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.request_header.v1.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchPartition:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    fetch_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The message offset."""
    partition_max_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum bytes to fetch from this partition.  See KIP-74 for cases where this limit may not be honored."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchTopic:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to fetch."""
    partitions: tuple[FetchPartition, ...]
    """The partitions to fetch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchRequest:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = False
    __api_key__: ClassVar[i16] = i16(1)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the follower, of -1 if this request is from a consumer."""
    max_wait_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum time in milliseconds to wait for the response."""
    min_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The minimum bytes to accumulate in the response."""
    topics: tuple[FetchTopic, ...]
    """The topics to fetch."""
