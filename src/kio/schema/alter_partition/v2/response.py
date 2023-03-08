"""
Generated from AlterPartitionResponse.json.
"""

# ruff: noqa: A003

import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i8
from kio.schema.primitive import i16
from kio.schema.primitive import i32
from kio.schema.response_header.v1.header import ResponseHeader
from kio.schema.types import BrokerId


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(56)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index"""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The partition level error code"""
    leader_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The broker ID of the leader."""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The leader epoch."""
    isr: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The in-sync replica IDs."""
    leader_recovery_state: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """1 if the partition is recovering from an unclean leader election; 0 otherwise."""
    partition_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The current epoch for the partition for KRaft controllers. The current ZK version for the legacy controllers."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(56)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    topic_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """The ID of the topic"""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterPartitionResponse:
    __version__: ClassVar[i16] = i16(2)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(56)
    __header_schema__: ClassVar[type[ResponseHeader]] = ResponseHeader
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top level response error code"""
    topics: tuple[TopicData, ...]
