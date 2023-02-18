"""
Generated from DeleteTopicsRequest.json.
"""
from dataclasses import dataclass
from dataclasses import field
from typing import ClassVar

from kio.schema.primitive import i32
from kio.schema.types import TopicName


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteTopicsRequest:
    __flexible__: ClassVar[bool] = True
    topic_names: tuple[TopicName, ...] = field(
        metadata={"kafka_type": "string"}, default=()
    )
    """The names of the topics to delete"""
    timeout_ms: i32 = field(metadata={"kafka_type": "int32"})
    """The length of time in milliseconds to wait for the deletions to complete."""
