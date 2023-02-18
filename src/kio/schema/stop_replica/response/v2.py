"""
Generated from StopReplicaResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaPartitionError:
    __flexible__: ClassVar[bool] = True
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_index: i32 = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The partition error code, or 0 if there was no partition error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaResponse:
    __flexible__: ClassVar[bool] = True
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The top-level error code, or 0 if there was no top-level error."""
    partition_errors: tuple[StopReplicaPartitionError, ...]
    """The responses for each partition."""
