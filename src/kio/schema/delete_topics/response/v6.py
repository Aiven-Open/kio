"""
Generated from DeleteTopicsResponse.json.
"""
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i16
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class DeletableTopicResult:
    __flexible__: ClassVar[bool] = True
    name: TopicName | None = field(metadata={"kafka_type": "string"})
    """The topic name"""
    topic_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """the unique topic ID"""
    error_code: i16 = field(metadata={"kafka_type": "int16"})
    """The deletion error, or 0 if the deletion succeeded."""
    error_message: str | None = field(metadata={"kafka_type": "string"}, default=None)
    """The error message, or null if there was no error."""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsResponse:
    __flexible__: ClassVar[bool] = True
    throttle_time_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The duration in milliseconds for which the request was throttled due to a quota violation, or zero if the request did not violate any quota."""
    responses: tuple[DeletableTopicResult, ...]
    """The results for each topic we tried to delete."""
