"""
Generated from ConsumerGroupHeartbeatRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/ConsumerGroupHeartbeatRequest.json
"""

# ruff: noqa: A003

import datetime
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import GroupId
from kio.schema.types import TopicName
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i32Timedelta


@dataclass(frozen=True, slots=True, kw_only=True)
class Assignor:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(68)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    name: str = field(metadata={"kafka_type": "string"})
    """The name of the assignor."""
    minimum_version: i16 = field(metadata={"kafka_type": "int16"})
    """The minimum supported version for the metadata."""
    maximum_version: i16 = field(metadata={"kafka_type": "int16"})
    """The maximum supported version for the metadata."""
    reason: i8 = field(metadata={"kafka_type": "int8"})
    """The reason of the metadata update."""
    metadata_version: i16 = field(metadata={"kafka_type": "int16"})
    """The version of the metadata."""
    metadata_bytes: bytes = field(metadata={"kafka_type": "bytes"})
    """The metadata."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartitions:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(68)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_id: uuid.UUID | None = field(metadata={"kafka_type": "uuid"})
    """The topic ID."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The partitions."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerGroupHeartbeatRequest:
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(68)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    group_id: GroupId = field(metadata={"kafka_type": "string"})
    """The group identifier."""
    member_id: str = field(metadata={"kafka_type": "string"})
    """The member id generated by the coordinator. The member id must be kept during the entire lifetime of the member."""
    member_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current member epoch; 0 to join the group; -1 to leave the group; -2 to indicate that the static member will rejoin."""
    instance_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """null if not provided or if it didn't change since the last heartbeat; the instance Id otherwise."""
    rack_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """null if not provided or if it didn't change since the last heartbeat; the rack ID of consumer otherwise."""
    rebalance_timeout: i32Timedelta = field(
        metadata={"kafka_type": "timedelta_i32"},
        default=i32Timedelta.parse(datetime.timedelta(milliseconds=-1)),
    )
    """-1 if it didn't chance since the last heartbeat; the maximum time in milliseconds that the coordinator will wait on the member to revoke its partitions otherwise."""
    subscribed_topic_names: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """null if it didn't change since the last heartbeat; the subscribed topic names otherwise."""
    subscribed_topic_regex: str | None = field(
        metadata={"kafka_type": "string"}, default=None
    )
    """null if it didn't change since the last heartbeat; the subscribed topic regex otherwise"""
    server_assignor: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """null if not used or if it didn't change since the last heartbeat; the server side assignor to use otherwise."""
    client_assignors: tuple[Assignor, ...]
    """null if not used or if it didn't change since the last heartbeat; the list of client-side assignors otherwise."""
    topic_partitions: tuple[TopicPartitions, ...]
    """null if it didn't change since the last heartbeat; the partitions owned by the member."""
