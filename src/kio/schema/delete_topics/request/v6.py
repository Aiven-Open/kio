"""
Generated from DeleteTopicsRequest.json.
"""
import uuid
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.entity import TopicName
from kio.schema.primitive import i32


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicState:
    __flexible__: ClassVar[bool] = True
    name: TopicName | None = field(metadata={"kafka_type": "string"}, default=None)
    """The topic name"""
    topic_id: uuid.UUID = field(metadata={"kafka_type": "uuid"})
    """The unique topic ID"""


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsRequest:
    __flexible__: ClassVar[bool] = True
    topics: tuple[DeleteTopicState, ...]
    """The name or topic ID of the topic"""
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The length of time in milliseconds to wait for the deletions to complete."""
