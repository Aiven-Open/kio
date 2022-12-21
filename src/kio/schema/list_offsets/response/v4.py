"""
Generated from ListOffsetsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsPartitionResponse:
    __flexible__: ClassVar[bool] = False
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The partition error code, or 0 if there was no error."""
    timestamp: int = field(metadata={"kafka_type": "int64"}, default=-1)
    """The timestamp associated with the returned offset."""
    offset: int = field(metadata={"kafka_type": "int64"}, default=-1)
    """The returned offset."""
    leader_epoch: int = field(metadata={"kafka_type": "int32"}, default=-1)


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsTopicResponse:
    __flexible__: ClassVar[bool] = False
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[ListOffsetsPartitionResponse, ...]
    """Each partition in the response."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ListOffsetsResponse:
    __flexible__: ClassVar[bool] = False
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[ListOffsetsTopicResponse, ...]
    """Each topic in the response."""
