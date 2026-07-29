"""
Generated from ``clients/src/main/resources/common/message/ConsumerProtocolAssignment.json``.
"""

from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.types import TopicName
from kio.static.constants import EntityType
from kio.static.primitive import i16
from kio.static.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class TopicPartition:
    __type__: ClassVar = EntityType.nested
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    topic: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partitions: tuple[i32, ...] = field(metadata={"kafka_type": "int32"}, default=())
    """The list of partitions assigned to this consumer."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ConsumerProtocolAssignment:
    __type__: ClassVar = EntityType.data
    __version__: ClassVar[i16] = i16(0)
    __flexible__: ClassVar[bool] = False
    assigned_partitions: tuple[TopicPartition, ...]
    """The list of topics and partitions assigned to this consumer."""
    user_data: bytes | None = field(metadata={"kafka_type": "bytes"}, default=None)
    """User data."""
