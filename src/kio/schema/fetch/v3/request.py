"""
Generated from FetchRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.primitive import i64
from kio.schema.types import BrokerId
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchPartition:
    __flexible__: ClassVar[bool] = False
    partition: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    fetch_offset: i64 = field(metadata={"kafka_type": "int64"})
    """The message offset."""
    partition_max_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum bytes to fetch from this partition.  See KIP-74 for cases where this limit may not be honored."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchTopic:
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to fetch."""
    partitions: tuple[FetchPartition, ...]
    """The partitions to fetch."""


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchRequest:
    __flexible__: ClassVar[bool] = False
    replica_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the follower, of -1 if this request is from a consumer."""
    max_wait_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The maximum time in milliseconds to wait for the response."""
    min_bytes: i32 = field(metadata={"kafka_type": "int32"})
    """The minimum bytes to accumulate in the response."""
    max_bytes: i32 = field(metadata={"kafka_type": "int32"}, default=i32(2147483647))
    """The maximum bytes to fetch.  See KIP-74 for cases where this limit may not be honored."""
    topics: tuple[FetchTopic, ...]
    """The topics to fetch."""
