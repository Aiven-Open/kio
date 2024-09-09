"""
Generated from ``clients/src/main/resources/common/message/ConsumerGroupDescribeResponse.json``.
"""

import uuid

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.errors import ErrorCode
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartitions:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(69)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The topic ID."""
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Assignment:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(69)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_partitions: tuple[TopicPartitions, ...]
    """The assigned topic-partitions to the member."""
    error: i8 = field(metadata={"kafka_type": "int8"})
    """The assigned error."""
    metadata_version: i32 = field(metadata={"kafka_type": "int32"})
    """The assignor metadata version."""
    metadata_bytes: bytes = field(metadata={"kafka_type": "bytes"})
    """The assignor metadata bytes."""


@dataclass(frozen=True, slots=True, kw_only=True)
class Member:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(69)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member ID."""
    instance_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The member instance ID."""
    rack_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The member rack ID."""
    member_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current member epoch."""
    client_id: str = field(metadata={"kafka_type": "string"})
    """The client ID."""
    client_host: str = field(metadata={"kafka_type": "string"})
    """The client host."""
    subscribed_topic_names: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The subscribed topic names."""
    subscribed_topic_regex: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """the subscribed topic regex otherwise or null of not provided."""
    assignment: Assignment
    """The current assignment."""
    target_assignment: Assignment
    """The target assignment."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DescribedGroup:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(69)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    error_code: ErrorCode = field(metadata={"kafka_type": "error_code"})
    """The describe error, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The top-level error message, or null if there was no error."""
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group ID string."""
    group_state: str = field(metadata={"kafka_type": "string"})
    """The group state string, or the empty string."""
    group_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The group epoch."""
    assignment_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The assignment epoch."""
    assignor_name: str = field(metadata={"kafka_type": "string"})
    """The selected assignor."""
    members: tuple[Member, ...]
    """The members."""
    authorized_operations: i32 = field(
        metadata={"kafka_type": "int32"}, default=i32(-2147483648)
    )
    """32-bit bitfield to represent authorized operations for this group."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerGroupDescribeResponse:
    __type__: ClassVar = EntityType.response
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(69)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time: i32Timedelta = field(metadata={"kafka_type": "timedelta_i32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    groups: tuple[DescribedGroup, ...]
    """Each described group."""
