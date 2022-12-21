"""
Generated from StopReplicaResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaPartitionError:
    __flexible__: ClassVar[bool] = False
    topic_name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name."""
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The partition error code, or 0 if there was no partition error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class StopReplicaResponse:
    __flexible__: ClassVar[bool] = False
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The top-level error code, or 0 if there was no top-level error."""
    partition_errors: tuple[StopReplicaPartitionError, ...]
    """The responses for each partition."""
