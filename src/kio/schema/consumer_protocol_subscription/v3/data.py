"""
Generated from ConsumerProtocolSubscription.json.

https://github.com/apache/kafka/tree/3.5.1/clients/src/main/resources/common/message/ConsumerProtocolSubscription.json
"""

# ruff: noqa: A003

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.types import TopicName
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartition:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerProtocolSubscription:
    __version__: ClassVar[i16] = i16(3)
    __flexible__: ClassVar[bool] = False
    topics: tuple[str, ...] = field(metadata={"kafka_type": "string"}, default=())
    user_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
    owned_partitions: tuple[TopicPartition, ...]
    generation_id: i32 = field(metadata={"kafka_type": "int32"}, default=i32(-1))
    rack_id: str | None = field(metadata={"kafka_type": "string"}, default=None)
