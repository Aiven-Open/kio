"""
Generated from ControlledShutdownResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class RemainingPartition:
    __flexible__: ClassVar[bool] = False
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The name of the topic."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The index of the partition."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ControlledShutdownResponse:
    __flexible__: ClassVar[bool] = False
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top-level error code."""
    remaining_partitions: tuple[RemainingPartition, ...]
    """The partitions that the broker still leads."""
