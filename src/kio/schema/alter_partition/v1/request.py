"""
Generated from AlterPartitionRequest.json.

https://github.com/apache/kafka/tree/3.6.0/clients/src/main/resources/common/message/AlterPartitionRequest.json
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.request_header.v2.header import RequestHeader
from kio.schema.types import BrokerId
from kio.schema.types import TopicName
from kio.static.primitive import i8
from kio.static.primitive import i16
from kio.static.primitive import i32
from kio.static.primitive import i64
from kio.static.protocol import ApiMessage


@dataclass(frozen=True, slots=True, kw_only=True)
class PartitionData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(56)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index"""
    leader_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The leader epoch of this partition"""
    new_isr: tuple[BrokerId, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The ISR for this partition. Deprecated since version 3."""
    leader_recovery_state: i8 = field(metadata={"kafka_type": "int8"}, default=i8(0))
    """1 if the partition is recovering from an unclean leader election; 0 otherwise."""
    partition_epoch: i32 = field(metadata={"kafka_type": "int32"})
    """The expected epoch of the partition which is being updated. For legacy cluster this is the ZkVersion in the LeaderAndIsr request."""


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicData:
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(56)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic to alter ISRs for"""
    partitions: tuple[PartitionData, ...]


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterPartitionRequest(ApiMessage):
    __version__: ClassVar[i16] = i16(1)
    __flexible__: ClassVar[bool] = True
    __api_key__: ClassVar[i16] = i16(56)
    __header_schema__: ClassVar[type[RequestHeader]] = RequestHeader
    broker_id: BrokerId = field(metadata={"kafka_type": "int32"})
    """The ID of the requesting broker"""
    broker_epoch: i64 = field(metadata={"kafka_type": "int64"}, default=i64(-1))
    """The epoch of the requesting broker"""
    topics: tuple[TopicData, ...]
