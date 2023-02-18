"""
Generated from ConsumerProtocolAssignment.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartition:
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerProtocolAssignment:
    __flexible__: ClassVar[bool] = False
    assigned_partitions: tuple[TopicPartition, ...]
    user_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
