"""
Generated from ``clients/src/main/resources/common/message/DescribeTopicPartitionsResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTopicPartitionsResponsePartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(75)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The partition error, or 0 if there was no error."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the leader broker."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    """The leader epoch of this partition."""
    replica_nodes: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of all nodes that host this partition."""
    isr_nodes: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of nodes that are in sync with the leader for this partition."""
    eligible_leader_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The new eligible leader replicas otherwise."""
    last_known_elr: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The last known ELR."""
    offline_replicas: tuple[BrokerId, ...] = field(
        metadata={"kafka_type": "int32"}, default=()
    )
    """The set of offline replicas of this partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTopicPartitionsResponseTopic:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(75)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The topic error, or 0 if there was no error."""
    name: TopicName | None = field(metadata={"kafka_type": "string"})
    """The topic name."""
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The topic id."""
    is_internal: bool = field(metadata={"kafka_type": "bool"}, default=False)
    """True if the topic is internal."""
    partitions: tuple[DescribeTopicPartitionsResponsePartition, ...]
    """Each partition in the topic."""
    topic_authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this topic."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Cursor:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(75)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The name for the first topic to process"""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index to start with"""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribeTopicPartitionsResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(75)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    topics: tuple[DescribeTopicPartitionsResponseTopic, ...]
    """Each topic in the response."""
    next_cursor: Cursor | None = field(default=None)
    """The next topic and partition index to fetch details for."""
