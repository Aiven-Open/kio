"""
Generated from ConsumerProtocolSubscription.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartition:
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerProtocolSubscription:
    __flexible__: ClassVar[bool] = False
    topics: tuple[str, ...] = field(metadata={"kafka_type": "string"}, default=())
    user_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
    owned_partitions: tuple[TopicPartition, ...]
