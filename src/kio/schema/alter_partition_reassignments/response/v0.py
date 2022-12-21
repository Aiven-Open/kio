"""
Generated from AlterPartitionReassignmentsResponse.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class ReassignablePartitionResponse:
    __flexible__: ClassVar[bool] = True
    partition_index: int = field(metadata={"kafka_type": "int32"})
    """The partition index."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The error code for this partition, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The error message for this partition, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class ReassignableTopicResponse:
    __flexible__: ClassVar[bool] = True
    name: TopicName = field(metadata={"kafka_type": "string"})
    """The topic name"""
    partitions: tuple[ReassignablePartitionResponse, ...]
    """The responses to partitions to reassign"""


@dataclass(frozen=True, slots=True, kw_only=True)
class AlterPartitionReassignmentsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: int = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    error_code: int = field(metadata={"kafka_type": "int16"})
    """The top-level error code, or 0 if there was no error."""
    error_message: str | None = field(metadata={"kafka_type": "string"})
    """The top-level error message, or null if there was no error."""
    responses: tuple[ReassignableTopicResponse, ...]
    """The responses to topics to reassign."""
