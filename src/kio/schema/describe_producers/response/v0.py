"""
Generated from DescribeProducersResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import ProducerId
from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class ProducerState:
    __flexible__: ClassVar[bool] = True
    producer_id: ProducerId = field(metadata={"kafka_type": "int64"})
    producer_epoch: int = field(metadata={"kafka_type": "int32"})
    last_sequence: int = field(metadata={"kafka_type": "int32"}, default=-1)
    last_timestamp: int = field(metadata={"kafka_type": "int64"}, default=-1)
    coordinator_epoch: int = field(metadata={"kafka_type": "int32"})
    current_txn_start_offset: int = field(metadata={"kafka_type": "int64"}, default=-1)


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionResponse:
    __flexible__: ClassVar[bool] = True
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: int = field(metadata={"kafka_type": "int16"})
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
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[TopicResponse, ...]
    """Each topic in the response."""
