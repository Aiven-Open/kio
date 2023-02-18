"""
Generated from DescribeProducersResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.primitive import i64


@dataclass(frozen=True, slots=True, kw_only=True)
class ProducerState:
    __flexible__: ClassVar[bool] = True
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    producer_epoch: i32 = field(metadata={"kafka_type": "int32"})
    last_sequence: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    last_timestamp: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    coordinator_epoch: i32 = field(metadata={"kafka_type": "int32"})
    current_txn_start_offset: i64 = field(
        metadata={"kafka_type": "int64"}, default=i64(-1)
    )


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionResponse:
    __flexible__: ClassVar[bool] = True
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The partition error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The partition error message, which may be null if no additional details are available"""
    active_producers: tuple[ProducerState, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicResponse:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[PartitionResponse, ...]
    """Each partition in the response."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeProducersResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[TopicResponse, ...]
    """Each topic in the response."""
